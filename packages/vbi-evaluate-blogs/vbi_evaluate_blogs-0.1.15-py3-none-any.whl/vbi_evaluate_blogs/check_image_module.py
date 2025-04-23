from urllib.parse import urlparse
import base64
import re
import logging
from typing import List, Dict, Optional
import requests
from langchain.schema import HumanMessage
from langchain.schema.messages import SystemMessage
from langchain_openai import AzureChatOpenAI

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """Class to handle image fetching, analysis and text-image alignment checking."""
    
    def __init__(self, text_llm: AzureChatOpenAI, image_llm: AzureChatOpenAI, language: str = "vi"):
        """
        Initialize the ImageAnalyzer with LLM models.
        
        Args:
            text_llm: LLM for text analysis
            image_llm: LLM with vision capabilities for image analysis
            language: Output language (default: Vietnamese)
        """
        self.text_llm = text_llm
        self.image_llm = image_llm
        self.language = language
        self.image_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg', 'bmp']
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate if a string is a proper URL with scheme and domain."""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False

    def get_base64_from_url(self, url: str, timeout: int = 10) -> Optional[str]:
        """
        Fetch an image from URL and convert to base64.
        
        Args:
            url: The URL of the image
            timeout: Request timeout in seconds
            
        Returns:
            Base64 encoded image or None if failed
        """
        # Clean URL of whitespace and newline characters
        clean_url = url.strip().replace('\n', '').replace('\r', '').replace('%0A', '')
        
        if not self.is_valid_url(clean_url):
            logger.warning(f"Invalid URL format: {clean_url}")
            return None
        
        try:
            response = requests.get(clean_url, timeout=timeout, 
                                   headers={'User-Agent': 'Mozilla/5.0 (compatible; ImageAnalyzer/1.0)'})
            response.raise_for_status()
            
            # Check if content type is an image
            if 'image' not in response.headers.get('Content-Type', ''):
                logger.warning(f"URL does not contain an image: {clean_url}")
                return None
                
            return base64.b64encode(response.content).decode('utf-8')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch image from {clean_url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing {clean_url}: {e}")
            return None

    def describe_image(self, url: str) -> str:
        """
        Get a detailed description of an image using the vision-capable LLM.
        
        Args:
            url: URL of the image to analyze
            
        Returns:
            Detailed description of the image in the specified language
        """
        base64_image = self.get_base64_from_url(url)
        if not base64_image:
            return f"Image at URL {url} is unavailable or could not be fetched."

        messages = [
            SystemMessage(content=f"You are an expert in analyzing images and text in documents. Provide outputs in {self.language}."),
            HumanMessage(content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "Please analyze the provided image in detail. "
                        "Describe the content, layout, colors, objects, text, and any other relevant features. "
                        "If the image contains text, extract and summarize it. "
                        "Provide a comprehensive and structured description."
                    )
                }
            ])
        ]

        try:
            response = self.image_llm.invoke(messages)
            return str(response.content)
        except Exception as e:
            logger.error(f"Error describing image {url}: {e}")
            return f"Failed to analyze image at {url}: {str(e)}"

    def extract_image_urls(self, content: str) -> List[str]:
        """
        Extract image URLs from content.
        
        Args:
            content: HTML or text content to search for image URLs
            
        Returns:
            List of found image URLs
        """
        # Create pattern with all supported image extensions
        extensions = '|'.join(self.image_extensions)
        pattern = rf'https?://[^\s\'"]+\.(?:{extensions})'
        
        # Find all image URLs
        image_urls = re.findall(pattern, content, re.IGNORECASE)
        return image_urls

    def extract_alt_texts(self, content: str) -> Dict[str, str]:
        """
        Extract alt text attributes for images in markdown content.
        
        This function identifies images in markdown format and extracts their alt text
        and source URL. It handles both standard markdown image syntax and HTML img tags.
        
        Args:
            content (str): The markdown content to analyze
            
        Returns:
            Dict[str, str]: A dictionary mapping image URLs to their alt text
        """
        alt_texts = {}
        
        # Match markdown image pattern ![alt](url)
        md_img_pattern = r'!\[([^\]]*)\]\(([^"\)\s]+)(?:\s+"[^"]*")?\)'
        md_matches = re.findall(md_img_pattern, content)
        
        # Match HTML img tag pattern <img src="url" alt="alt text" />
        html_img_pattern = r'<img[^>]*src=["\'](.*?)["\'][^>]*alt=["\'](.*?)["\'][^>]*/?>'
        html_matches = re.findall(html_img_pattern, content)
        # Also match when alt comes before src
        html_img_pattern_alt_first = r'<img[^>]*alt=["\'](.*?)["\'][^>]*src=["\'](.*?)["\'][^>]*/?>'
        html_alt_first_matches = re.findall(html_img_pattern_alt_first, content)
        
        # Process markdown matches
        for alt, src in md_matches:
            # Clean and normalize URL
            src = src.strip()
            if self._is_image_file(src):
                alt_texts[src] = alt
        
        # Process HTML matches
        for src, alt in html_matches:
            if self._is_image_file(src):
                alt_texts[src] = alt
        
        # Process HTML matches where alt comes before src
        for alt, src in html_alt_first_matches:
            if self._is_image_file(src) and src not in alt_texts:
                alt_texts[src] = alt
                
        return alt_texts

    def _is_image_file(self, url: str) -> bool:
        """
        Check if the URL points to an image file.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL is an image file, False otherwise
        """
        # Handle URL parameters and fragments
        base_url = url.split('?')[0].split('#')[0]
        
        # Check if URL has a file extension that matches known image types
        return any(base_url.lower().endswith(ext) for ext in self.image_extensions)

    def check_image(self, content: str, window_size: int = 500) -> str:
        """
        Analyze image-text alignment in content.
        
        Args:
            content: The content to analyze
            window_size: Character window around images to consider as context
            
        Returns:
            Analysis of image-text alignment
        """
        image_urls = self.extract_image_urls(content)
        alt_texts = self.extract_alt_texts(content)
        
        if not image_urls:
            return "No image URLs found in the content."
            
        logger.info(f"Found {len(image_urls)} image URLs")
        
        # Copy original content for replacement
        processed_content = content
        
        # Process each image
        for idx, image_url in enumerate(image_urls):
            # Get image description
            logger.info(f"Processing image {idx+1}/{len(image_urls)}: {image_url}")
            description = self.describe_image(image_url)
            
            # Get alt text if available
            alt_text = alt_texts.get(image_url, "")
            if alt_text:
                description += f"\n\nExisting alt text: {alt_text}"
                
            # Create describe tag with index for easier reference
            describe_tag = f"<describe_image_{idx+1}>{description}</describe_image_{idx+1}>"
            
            # Find position of URL in content
            url_pos = processed_content.find(image_url)
            if url_pos == -1:
                logger.warning(f"URL not found in content: {image_url}")
                continue
                
            # Extract surrounding context
            start = max(0, url_pos - window_size)
            end = min(len(processed_content), url_pos + len(image_url) + window_size)
            context = processed_content[start:end]
            
            # Replace URL with description tag in the context
            context = context.replace(image_url, describe_tag)
            
            # Update the processed content
            processed_content = processed_content[:start] + context + processed_content[end:]

        # Create improved analysis prompt
        prompt = """
<prompt>
  <task>
    Bạn là một chuyên gia AI có khả năng đánh giá mức độ bổ trợ giữa hình ảnh và văn bản trong nội dung web. Nhiệm vụ của bạn là phân tích mức độ liên kết và hỗ trợ giữa các hình ảnh (được mô tả trong thẻ) và văn bản xung quanh, đồng thời đánh giá và cải thiện các thuộc tính alt text.
  </task>

  <input_format>
    Nội dung bao gồm đoạn văn bản với các mô tả hình ảnh được đánh dấu bằng thẻ <describe_image_n>...</describe_image_n> đã thay thế cho URL gốc của hình ảnh. Số n là chỉ số của hình ảnh trong nội dung.
  </input_format>

  <output_format>
    Đối với mỗi hình ảnh, hãy cung cấp phân tích như sau:

    ### Hình ảnh [index]:
    - **Mô tả tóm tắt:** (Tóm tắt ngắn gọn nội dung hình ảnh)
    - **Ngữ cảnh văn bản:** (Trích đoạn văn bản liên quan xung quanh hình ảnh)
    - **Mức độ bổ trợ:** [1-5]
    - **Phân tích:** (Giải thích chi tiết mối quan hệ giữa hình ảnh và văn bản)
    - **Đánh giá alt text:** [1-5] (nếu có)
    - **Đề xuất alt text:** (Đề xuất alt text tối ưu cho hình ảnh)
    - **Cải thiện khuyến nghị:** (Gợi ý cải thiện sự liên kết giữa hình ảnh và văn bản)
  </output_format>

  <scoring_criteria>
    - Mức độ bổ trợ:
      5: Hoàn hảo - Hình ảnh và văn bản bổ sung cho nhau một cách tối ưu, tạo giá trị gia tăng đáng kể
      4: Tốt - Hình ảnh và văn bản có mối liên hệ rõ ràng, hỗ trợ hiểu biết
      3: Đủ - Hình ảnh và văn bản liên quan nhưng không hỗ trợ sâu sắc
      2: Yếu - Có liên quan lỏng lẻo, không thực sự bổ sung
      1: Kém - Không liên quan hoặc gây hiểu nhầm
      
    - Đánh giá alt text:
      5: Mô tả đầy đủ, súc tích và chính xác nội dung và chức năng của hình ảnh
      4: Mô tả tốt nhưng có thể cải thiện
      3: Mô tả cơ bản nhưng thiếu chi tiết quan trọng
      2: Mô tả không đầy đủ hoặc quá chung chung
      1: Thiếu hoặc không liên quan đến nội dung hình ảnh
  </scoring_criteria>
</prompt>
        """

        # Submit for analysis
        messages = [
            SystemMessage(content=f"You are an expert in evaluating image-text alignment. Provide analysis in {self.language}."),
            HumanMessage(content=prompt + "\n\n" + processed_content)
        ]

        try:
            response = self.text_llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error in analyzing image-text alignment: {e}")
            return f"Failed to analyze image-text alignment: {str(e)}"

    def suggest_image_improvements(self, content: str) -> str:
        """
        Suggest improvements for images in the content based on the analysis.
        
        Args:
            content: The content with images to analyze
            
        Returns:
            Suggestions for improving images and their integration with text
        """
        # First, get the alignment analysis
        alignment_analysis = self.check_image_text_alignment(content)
        
        # Now ask for specific improvements
        improvement_prompt = f"""
Based on the following image-text alignment analysis, provide specific recommendations 
for improving the visual content strategy:

{alignment_analysis}

Please include:
1. Overall assessment of image usage in the content
2. Specific recommendations for each problematic image
3. General best practices for better image-text integration
4. Suggestions for alternative or additional images that would enhance the content
5. Recommendations for improving alt text across all images

Format your response as a comprehensive improvement plan, prioritizing changes 
that would have the greatest impact on user experience and accessibility.
"""

        messages = [
            SystemMessage(content=f"You are an expert in visual content strategy and accessibility. Provide recommendations in {self.language}."),
            HumanMessage(content=improvement_prompt)
        ]

        try:
            response = self.text_llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating improvement suggestions: {e}")
            return f"Failed to generate improvement suggestions: {str(e)}"
    
    def analyze_image_seo(self, content: str) -> str:
        """
        Analyze SEO aspects of images in the content.
        
        Args:
            content: The HTML or text content containing images
            
        Returns:
            Detailed SEO analysis of images
        """
        image_urls = self.extract_image_urls(content)
        alt_texts = self.extract_alt_texts(content)
        
        if not image_urls:
            return "Không tìm thấy URL hình ảnh trong nội dung."
        
        logger.info(f"Phân tích SEO cho {len(image_urls)} hình ảnh")
        
        # Build prompt for SEO analysis
        seo_prompt = """
    <prompt>
    <task>
        Bạn là một chuyên gia phân tích SEO cho hình ảnh trong nội dung web. Nhiệm vụ của bạn là đánh giá các yếu tố SEO của từng hình ảnh và đưa ra các đề xuất cải thiện.
    </task>

    <input_format>
        Nội dung bao gồm các mô tả hình ảnh kèm theo URL và alt text (nếu có). Mỗi hình ảnh được đánh dấu bằng thẻ <image_seo_n>...</image_seo_n> với n là chỉ số của hình ảnh.
    </input_format>

    <output_format>
        ### Báo cáo SEO hình ảnh tổng quan:
        - **Số lượng hình ảnh được phân tích:** [số lượng]
        - **Điểm SEO trung bình:** [1-10]
        - **Tỷ lệ hình ảnh có alt text:** [%]
        - **Các vấn đề phổ biến:** [liệt kê]
        
        Cho mỗi hình ảnh:
        
        ### Hình ảnh [index]:
        - **URL:** [URL hình ảnh]
        - **Alt text:** [alt text nếu có, hoặc "Không có"]
        - **Tên file:** [tên file rút ra từ URL]
        - **Điểm SEO:** [1-10]
        
        **Phân tích:**
        1. **Alt text:** [đánh giá chất lượng alt text, độ dài, từ khóa]
        2. **Tên file:** [đánh giá tính tối ưu của tên file]
        3. **Ngữ cảnh:** [đánh giá sự phù hợp với nội dung xung quanh]
        4. **Mô tả hình ảnh:** [dựa vào phân tích nội dung hình ảnh từ mục <description>]
        
        **Đề xuất cải thiện:**
        - [Đề xuất alt text tối ưu hơn]
        - [Đề xuất tên file tối ưu hơn nếu cần]
        - [Các đề xuất khác về vị trí, kích thước, định dạng...]
    </output_format>

    <scoring_criteria>
        - Điểm SEO (1-10):
        10: Hoàn hảo - Tối ưu đầy đủ về alt text, tên file, ngữ cảnh và liên quan đến từ khóa
        8-9: Rất tốt - Hầu hết yếu tố đã tối ưu nhưng còn cải thiện nhỏ
        6-7: Tốt - Cơ bản được tối ưu nhưng cần cải thiện đáng kể
        4-5: Trung bình - Nhiều yếu tố chưa tối ưu
        2-3: Yếu - Hầu hết yếu tố SEO chưa được áp dụng
        1: Rất kém - Không có bất kỳ tối ưu SEO nào
    </scoring_criteria>
    </prompt>
        """
        
        # Process each image and build input for analysis
        processed_content = ""
        
        for idx, image_url in enumerate(image_urls):
            logger.info(f"Đang xử lý hình ảnh {idx+1}/{len(image_urls)}: {image_url}")
            
            # Get image description using existing method
            description = self.describe_image(image_url)
            
            # Extract filename from URL
            try:
                filename = image_url.split('/')[-1]
            except:
                filename = "unknown"
            
            # Get alt text if available
            alt_text = alt_texts.get(image_url, "Không có")
            
            # Build image SEO analysis block
            image_block = f"""
    <image_seo_{idx+1}>
    <url>{image_url}</url>
    <filename>{filename}</filename>
    <alt_text>{alt_text}</alt_text>
    <description>{description}</description>
    </image_seo_{idx+1}>
            """
            
            processed_content += image_block
        
        # Submit for SEO analysis
        messages = [
            SystemMessage(content=f"Bạn là chuyên gia phân tích SEO cho hình ảnh. Cung cấp phân tích chi tiết bằng {self.language}."),
            HumanMessage(content=seo_prompt + "\n\n" + processed_content)
        ]

        try:
            response = self.text_llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Lỗi khi phân tích SEO hình ảnh: {e}")
            return f"Không thể hoàn thành phân tích SEO hình ảnh: {str(e)}"
    
    def check_image_full_report(self, content: str) -> str:
        """
        Generate a comprehensive report on images including alignment with text and SEO aspects.
        
        Args:
            content: The HTML or text content containing images
            
        Returns:
            Comprehensive analysis of images
        """
        alignment_analysis = self.check_image(content)
        seo_analysis = self.analyze_image_seo(content)
        
        report_prompt = f"""
    Dựa trên hai phân tích sau đây về hình ảnh trong nội dung web:

    1. Phân tích mối quan hệ hình ảnh - văn bản:
    {alignment_analysis}

    2. Phân tích SEO hình ảnh:
    {seo_analysis}

    Hãy tổng hợp thành một báo cáo toàn diện về hình ảnh trong nội dung, bao gồm:

    1. Tổng quan về chất lượng và hiệu quả của hình ảnh
    2. Những điểm mạnh cần duy trì
    3. Các vấn đề chính cần khắc phục
    4. Kế hoạch hành động ưu tiên để cải thiện
    5. Dự đoán tác động của những cải thiện đối với hiệu suất SEO và trải nghiệm người dùng

    Báo cáo nên đánh giá chi tiết từng hình ảnh, nhấn mạnh các cơ hội tối ưu hóa quan trọng nhất.
        """
        
        # Submit for comprehensive analysis
        messages = [
            SystemMessage(content=f"Bạn là chuyên gia phân tích nội dung và SEO. Cung cấp báo cáo chuyên sâu bằng {self.language}."),
            HumanMessage(content=report_prompt)
        ]

        try:
            response = self.text_llm.invoke(messages)
            return f"{response.content}\n\n---CHI TIẾT---\n{alignment_analysis}\n{seo_analysis}"
        except Exception as e:
            logger.error(f"Lỗi khi tạo báo cáo tổng hợp: {e}")
            return f"Không thể tạo báo cáo tổng hợp về hình ảnh: {str(e)}"
        
def check_image(text_llm, image_llm, content: str) -> str:
    image_analyzer = ImageAnalyzer(text_llm, image_llm)
    res = image_analyzer
    return image_analyzer.check_image_full_report(content)

if __name__ == "__main__":
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()

    image_llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model="gpt-4o-mini",
            api_version="2024-08-01-preview",
            temperature=0.7,
            max_tokens=16000
        )

    text_llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            model="o3-mini",
            api_version="2024-12-01-preview",
        )
    
    content = "![Cover Image](https://statics.gemxresearch.com/images/2025/04/11/154715/capwheel-series-pancake-swap.jpg)\n\n# CapWheel Series: PancakeSwap và token $CAKE\n\n **CapWheel Series** là chuỗi bài viết chuyên sâu [phân tích](https://gfiresearch.net/analysis) cách các dự án thiết kế mô hình Tokenomics và sản phẩm để khai thác giá trị cho token của họ. Mục tiêu của series này là cung cấp cái nhìn sâu sắc về giá trị nội tại của token, giúp đánh giá tiềm năng dài hạn của các dự án, thay vì chỉ chú trọng vào biến động ngắn hạn trên thị trường. CapWheel Series tập trung vào việc các dự án xây dựng cơ chế tích lũy giá trị qua các mô hình Tokenomics, thay vì phụ thuộc vào các yếu tố bên ngoài như tình hình thị trường chung hay sự tác động của các yếu tố đầu cơ. \n ## Điểm nổi bật\n\n- Pancake nổi bật so với các sàn DEX khác nhờ hệ sinh thái đa dạng, tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn trong mô hình Mint &amp; Burn của CAKE. Tuy nhiên, phần lớn lượng CAKE được Burn vẫn đến từ các hoạt động DEX, trong khi các sản phẩm khác chỉ đóng góp khoảng 11% vào tổng lượng Burn.\n\n\n- Đề xuất loại bỏ veCAKE được đưa ra với mục tiêu kiểm soát nguồn cung hiệu quả hơn, nhưng lại vấp phải tranh cãi gay gắt về tính phi tập trung. Pancake bị nghi ngờ đã có những động thái không minh bạch nhằm giảm sức ép từ các Liquid Wrappers trước khi đề xuất được đưa vào biểu quyết, làm dấy lên nhiều lo ngại trong cộng đồng.\n\n\n \n ## Tổng quan về PancakeSwap\n\nPancakeSwap hiện là sàn giao dịch phi tập trung (DEX) hàng đầu trên BNB Smart Chain, ghi dấu ấn với khối lượng giao dịch vượt trội, khẳng định vị thế tiên phong trong thị trường tài chính phi tập trung (DeFi). Với sự đổi mới không ngừng, PancakeSwap mang đến một hệ sinh thái đa dạng, tối ưu hóa trải nghiệm cho người dùng, nhà phát triển và nhà cung cấp thanh khoản.\n\nCác \n\nsản phẩm \n\ntrong hệ sinh thái PancakeSwap\n\nPancakeSwap cung cấp một loạt sản phẩm tiên tiến, được thiết kế để đáp ứng nhu cầu đa dạng của cộng đồng DeFi. Dưới đây là những điểm nhấn quan trọng:\n\nAMM Swap\n\nKế thừa từ Uniswap, PancakeSwap không chỉ tái hiện đầy đủ các tính năng cốt lõi mà còn nâng tầm với phiên bản V4, mang đến những cải tiến đột phá:\n\n- Hooks: Các hợp đồng thông minh bên ngoài cho phép tùy chỉnh linh hoạt các hồ thanh khoản, hỗ trợ phí động (thấp đến 0%), công cụ giao dịch nâng cao (lệnh giới hạn, chốt lời, TWAMM, hoàn phí), và tạo doanh thu cho nhà phát triển, thúc đẩy đổi mới.\n\n\n- Đa dạng Liquidity Pool tích hợp liền mạch với HOOKS như Concentrated Liquidity Automated Market Maker (CLAMM), Liquidity Book AMM (LBAMM) hay các Liquidity Pool có thiết kế mở, sẵn sàng cho các mô hình AMM mới, đáp ứng nhu cầu thị trường.\n\n\n- Donate: Khuyến khích nhà cung cấp thanh khoản trong phạm vi giá phù hợp, tăng lợi nhuận và sự tham gia.\n\n\n- Singleton: Gộp tất cả hồ thanh khoản vào một hợp đồng, giảm 99% chi phí tạo hồ và tối ưu gas cho giao dịch đa bước.\n\n\n- Flash Accounting: Tối ưu gas bằng cách tính toán số dư ròng và thanh toán tập trung, giảm chi phí so với mô hình cũ.\n\n\n- ERC-6909: Chuẩn đa token, quản lý token thay thế và không thay thế trong một hợp đồng, tăng hiệu quả, giảm chi phí.\n\n\n- Token Gas Gốc: Hỗ trợ giao dịch với token gas gốc, giảm chi phí và cải thiện trải nghiệm người dùng.\n\n\n- Mã Nguồn Mở: Khuyến khích nhà phát triển đổi mới và hợp tác thông qua giấy phép mở.\n\n\n- Chương trình Nhà phát triển: Quỹ 500.000 USD hỗ trợ chiến dịch tăng trưởng, hackathon, đại sứ phát triển, và tài trợ CAKE, thúc đẩy sáng tạo cộng đồng.\n\n\nEarn\n\n**Add LP &amp; Farming**Tương tự như các AMM Dex khác, người dùng có thể add liquid vào các liquidity pools ở trong Pancake và stake LP để farm ra CAKE từ lượng Emission.\n\n![](https://statics.gemxresearch.com/images/2025/04/11/154948/ADD-LP.png)  **Staking &amp; Syrup Pool**Syrup Pool là một sản phẩm staking của PancakeSwap, cho phép người dùng khóa CAKE hoặc các token khác để nhận phần thưởng dưới dạng CAKE hoặc token từ các dự án đối tác. Đây là cách đơn giản để kiếm lợi nhuận thụ động, đồng thời hỗ trợ hệ sinh thái PancakeSwap. Có hai loại pool chính:\n\n- CAKE Pool: Stake CAKE để nhận CAKE hoặc iCAKE (dùng cho IFO), chia thành Flexible Staking (rút bất kỳ lúc nào, APR thấp hơn) và Fixed-Term Staking (khóa cố định 1-52 tuần, APR cao hơn, tự động gia hạn trừ khi rút).\n\n\n- Non-CAKE Pool: Stake token từ dự án đối tác để nhận phần thưởng là token dự án đó hoặc CAKE, thường có thời hạn cố định.\n\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152622/Syrup Pool.png)  **IFO**Initial Farm Offering (IFO) của PancakeSwap là một cơ hội độc đáo để người dùng tiếp cận sớm các token mới, tương tự IDO nhưng được thiết kế riêng với sự tham gia thông qua CAKE, mang đến tiềm năng lợi nhuận hấp dẫn.\n\nĐể tham gia, người dùng cần khóa CAKE trong để nhận veCAKE, từ đó tạo ra iCAKE – chỉ số quyết định hạn mức tham gia IFO, với số lượng và thời gian khóa càng lớn\n\n thì iCAKE càng cao, mở rộng cơ hội trong Public Sale. Ngoài ra, cần tạo NFT Profile với một khoản phí nhỏ bằng CAKE, được sử dụng để đốt, góp phần giảm nguồn cung token và tăng giá trị dài hạn cho hệ sinh thái\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152744/ifo.png)  Play**Prediction**Prediction của PancakeSwap là một trò chơi dự đoán phi tập trung, đơn giản và thú vị, cho phép người dùng dự đoán giá BNBUSD, CAKEUSD hoặc ETHUSD sẽ tăng (UP) hay giảm (DOWN) trong các vòng kéo dài 5 phút (hoặc 10 phút trên zkSync). Người chơi đặt cược bằng BNB, CAKE hoặc ETH tùy thuộc vào thị trường, và nếu dự đoán đúng, họ chia sẻ quỹ thưởng của vòng.\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152822/prediction.png)  **Lottery**Lottery của PancakeSwap là trò chơi minh bạch, dễ tham gia, cho phép người dùng mua vé bằng CAKE (giá ~5 USD/vé, tối đa 100 vé/lần) để có cơ hội nhận thưởng lớn. Người chơi chọn 6 số, khớp càng nhiều số với kết quả ngẫu nhiên (dùng Chainlink VRF) càng nhận thưởng cao, từ giải nhỏ đến độc đắc. Tổng giải thưởng gồm CAKE từ vé bán và 10,000 CAKE bổ sung mỗi 2 ngày. Mua nhiều vé được chiết khấu, nhưng tăng nhẹ phí giao dịch. Một phần CAKE được đốt để giảm phát. Mỗi vòng kéo dài 12 giờ, vé không hoàn lại, kết quả kiểm tra thủ công. Lottery v2 tăng số khớp từ 4 lên 6, nâng cơ hội trúng giải nhỏ và tích lũy quỹ lớn hơn.\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152856/lottery.png)   \n ## Vậy PancakeSwap Caputure Value cho CAKE như thế nào?\n\nPancakeSwap đang tạo nên một cuộc cách mạng với mô hình Mint &amp; Burn kết hợp cùng veCAKE và hệ thống biểu quyết gauges, trao quyền cho người sở hữu CAKE để định hình tương lai của các liquidity pool. Bằng cách bỏ phiếu, veCAKE Holder có thể phân bổ CAKE Emission, ưu tiên các pool hoặc dự án yêu thích, mở ra cơ hội tối ưu hóa phần thưởng. Với veCAKE, bạn không chỉ là người tham gia mà còn là người dẫn dắt hệ sinh thái!\n\nveCAKE\n\n Holders có thể:\n\n- **Điều khiển Emission\n\n**: Trực tiếp quyết định cách phân bổ CAKE cho từng pool thanh khoản, dựa trên quyền biểu quyết tỷ lệ với số dư veCAKE. Quyền lực của bạn càng lớn, tác động càng sâu!\n\n\n- **Hợp tác với giao thức bên thứ ba\n\n**: Ủy quyền veCAKE cho các Liquid Wrappers hoặc thị trường Bribe để tự động hóa biểu quyết, nhận phần thưởng hấp dẫn hơn.\n\n\n- **Chinh phục hệ sinh thái PancakeSwap\n\n**: Power từ veCAKE (số lượng CAKE * thời gian lock) sẽ là thông số cho iCAKE (dùng cho IFO), bCAKE (dùng cho boosting yields farming).\n\n\nCơ chế Mint &amp; Burn – Tăng giá trị bền vững: Ngoài việc phân phối phần thưởng qua các sản phẩm, PancakeSwap đốt CAKE từ nhiều nguồn để giảm nguồn cung, đẩy giá trị lâu dài:\n\n- 0.001-0.23% phí giao dịch trên Exchange V3 (trừ Aptos).\n\n\n- 0.0575% phí giao dịch trên Exchange V2.\n\n\n- 0.004-0.02% phí từ StableSwap.\n\n\n- 20% lợi nhuận từ Perpetual Trading.\n\n\n- 100% phí hiệu suất CAKE từ IFO.\n\n\n- 100% CAKE dùng cho Profile Creation và NFT minting.\n\n\n- 100% CAKE từ người thắng Farm Auctions.\n\n\n- 2% doanh thu bán NFT trên NFT Market.\n\n\n- 20% CAKE từ \n\nviệc mua vé Lottery.\n\n\n- 3% mỗi \n\nround BNB/CAKE Prediction Markets\n\n dùng mua lại CAKE để burn.\n\n\n- 80% doanh thu từ bán tên miền .cake.\n\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152944/tokenomic.png)  Đề xuất bỏ veTOKEN\n\nDù mô hình veCAKE ra mắt năm 2023 từng tạo dấu ấn với quyền biểu quyết mạnh mẽ, PancakeSwap nay đưa ra Đề xuất Tokenomics 3.0, quyết định gỡ bỏ hệ thống này để khắc phục những hạn chế cản bước hệ sinh thái.\n\nTrước hết, veCAKE tạo ra hệ thống quản trị phức tạp, yêu cầu khóa token dài hạn, khiến nhiều người dùng khó tiếp cận và làm giảm sự tham gia cộng đồng. Thứ hai, \n\ncơ chế gauges phân bổ phần thưởng thiếu hiệu quả\n\n, khi các pool thanh khoản nhỏ nhận tới 40% CAKE Emission nhưng chỉ đóng góp dưới 2% vào doanh thu, gây lãng phí tài nguyên.\n\nBên cạnh đó, việc khóa CAKE dài hạn làm mất tính linh hoạt, hạn chế quyền tự do sở hữu tài sản. Cuối cùng, sự thiếu đồng bộ giữa Emission và giá trị kinh tế từ các pool tạo ra mất cân bằng, ảnh hưởng đến lợi ích chung.\n\nVới Tokenomics 3.0, PancakeSwap mở ra một kỷ nguyên mới, tập trung vào bốn mục tiêu lớn lao:\n\n- Tăng quyền sở hữu thực sự: Xóa bỏ staking CAKE, veCAKE, gauges và chia sẻ doanh thu, trao trả tự do sử dụng token cho người dùng mà không cần khóa dài hạn.\n\n\n- Đơn giản hóa quản trị: Thay thế mô hình veCAKE rườm rà bằng hệ thống linh hoạt, chỉ cần stake CAKE trong thời gian biểu quyết, mở cửa cho mọi người tham gia dễ dàng.\n\n\n- Tăng trưởng bền vững: \n\nĐặt mục tiêu giảm phát 4%/năm\n\n, giảm 20% nguồn cung CAKE đến 2030. Lượng Emission CAKE hàng ngày giảm từ 40,000 xuống 22,500 qua ba giai đoạn, được đội ngũ quản lý dựa trên dữ liệu thị trường thời gian thực, ưu tiên pool thanh khoản lớn để tăng hiệu quả 30-40%. \n\nToàn bộ phí giao dịch chuyển sang đốt CAKE, nâng tỷ lệ đốt ở một số pool từ 10% lên 15\n\n%.\n\n\n- Hỗ trợ cộng đồng: Mở khóa toàn bộ CAKE đã stake và veCAKE mà không phạt, với thời hạn rút 6 tháng qua giao diện PancakeSwap. Người dùng veCAKE từ bên thứ ba (như CakePie, StakeDAO) sẽ chờ đối tác triển khai rút.\n\n\n \n ## Onchain Insights\n\n \n ### Các sản phẩm\n\nChúng ta đã nắm rõ cách CAKE tạo giá trị thông qua veTOKEN và cơ chế Mint &amp; Burn trong hệ sinh thái PancakeSwap. Xét về sản phẩm Lottery, doanh thu từ bán vé (Ticket Sale) trong 90 ngày từ 03/01 đến 14/04/2024 cho thấy xu hướng tăng trưởng không ổn định, với những giai đoạn tăng giảm rõ rệt. Cụ thể, Lottery ghi nhận các đợt tăng trưởng mạnh như 200% vào đầu tháng 1, 100% vào đầu tháng 2 và giữa tháng 3, nhưng cũng đối mặt với những đợt sụt giảm đáng kể từ 33% đến 50%, đặc biệt giảm mạnh vào cuối tháng 3 và đầu tháng 4. Dù có phục hồi nhẹ 50% vào ngày 14/4, mức tăng này không đủ để bù đắp cho sự sụt giảm trước đó, cho thấy Lottery chưa tạo được sức hút bền vững.\n\nĐối với sản phẩm Prediction, phí giao dịch trên BNB Chain (tính bằng USD) từ ngày 01/01/2024 đến 08/04/2024 cho thấy xu hướng tăng trưởng mạnh mẽ ban đầu, sau đó giảm dần nhưng vẫn duy trì ở mức cao hơn so với đầu kỳ. Cụ thể, phí giao dịch tăng đột biến từ 15K USD vào ngày 01/01 lên mức đỉnh 157.9K USD vào ngày 24/01, tương ứng với mức tăng trưởng ấn tượng 952.67%. Tuy nhiên, sau khi đạt đỉnh, phí bắt đầu giảm dần, dao động từ 149.4K USD (ngày 07/02) xuống 117K USD (ngày 07/03), rồi phục hồi nhẹ lên 123.6K USD (ngày 14/03), trước khi tiếp tục giảm còn 91.1K USD vào ngày 08/04. Từ mức đỉnh đến cuối kỳ, phí giảm 42.30%, tương đương 66.8K USD. Dù vậy, so với đầu kỳ, phí giao dịch vẫn tăng trưởng mạnh 507.33%, từ 15K USD lên 91.1K USD.\n\nTại Perp, từ năm 2023 đến nay, mức phí thu được đạt đỉnh vào cuối quý 1/2024 với tổng cộng $330,673, ghi nhận mức tăng trưởng ấn tượng 1059.6% so với tháng 4/2023. Tuy nhiên, từ quý 2/2024, nguồn phí này bắt đầu suy giảm và kéo dài đến thời điểm hiện tại. So với mức phí cao nhất mọi thời đại (ATH) vào ngày 08/03/2024, con số này đã giảm mạnh xuống còn $20,451, tương ứng với mức giảm 93.8%. Về đóng góp, phần lớn phí đến từ BSC và ARB, trong khi OPBNB và Base chỉ chiếm một phần rất nhỏ, gần như không đáng kể trong tổng thể.\n\n \n ### Token\n\nVề lượng CAKE, hơn 93% được khóa để nhận veCAKE, trong khi 6.7% còn lại được phân bổ vào các Pool khác nhau (CAKE Pool). Từ tháng 1/2024 đến nay, xu hướng Net Mint của CAKE chủ yếu âm, cho thấy nguồn cung đang giảm phát một cách tích cực. Điều này phản ánh các sản phẩm trong hệ sinh thái CAKE vẫn duy trì đủ nhu cầu để thúc đẩy lượng Burn hàng tuần.\n\nDù PancakeSwap sở hữu nhiều sản phẩm đa dạng ngoài AMM và tích hợp chúng vào cơ chế Mint &amp; Burn, phần lớn lượng Burn lại đến từ hoạt động trên AMM Dex, trong khi các sản phẩm khác chỉ đóng góp khoảng 11.1% vào quá trình Burn. Điều này cho thấy AMM vẫn là động lực chính trong việc duy trì cơ chế giảm phát của CAKE.\n\n \n ## Tổng kết\n\nMô hình của Pancake nổi bật với sự đa dạng vượt trội so với các sàn DEX khác, không chỉ dừng lại ở DEX mà còn tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn, tạo sự cân bằng với lượng Emission để thu hút thanh khoản. Điểm nhấn là cơ chế veTOKEN, về lý thuyết, giúp khóa nguồn cung, giảm áp lực bán tháo lên biểu đồ giá. Tuy nhiên, thực tế lại cho thấy veTOKEN gây ra không ít trở ngại trong việc điều phối Emission, dẫn đến hạn chế cho các Liquidity Pools có TVL thấp, làm dấy lên những thách thức trong vận hành.\n\nDù Pancake hướng đến xây dựng một hệ sinh thái linh hoạt, bền vững, ưu tiên lợi ích cộng đồng và hiệu quả dài hạn, nhưng các đề xuất gần đây lại vấp phải tranh cãi xoay quanh tính phi tập trung và niềm tin từ cộng đồng. Những cuộc tranh luận này phản ánh sự cạnh tranh khốc liệt và cả những \"trò chơi chính trị\" trong nội bộ hệ sinh thái.\n\nMột vấn đề đáng chú ý là sự xuất hiện của các Liquid Wrappers – một hiện tượng phổ biến trong các dự án áp dụng mô hình veTOKEN, nhằm chiếm quyền sở hữu lượng lớn veTOKEN. Tuy nhiên, Pancake bị nghi ngờ đã âm thầm tích lũy CAKE để nâng tỷ lệ sở hữu veTOKEN lên gần 50%, vượt mặt các Liquid Wrappers. Đỉnh điểm là đề xuất loại bỏ hoàn toàn veTOKEN, gây ra nhiều tranh cãi.\n\n [Twitter Post](https://twitter.com/defiwars_/status/1909955376147059114)Nếu đề xuất này được thông qua, các Liquid Wrappers phụ thuộc vào veTOKEN sẽ đối mặt với nguy cơ sụp đổ hoàn toàn, do bản chất tồn tại của chúng dựa vào lượng veTOKEN nắm giữ. Mặt khác, việc loại bỏ veTOKEN có thể mang lại lợi ích lớn hơn cho Pancake, củng cố mô hình Mint &amp; Burn và gia tăng giá trị cho CAKE. Tuy nhiên, động thái này không chỉ là một quyết định chiến lược mà còn là một bước đi đầy rủi ro, có thể định hình lại niềm tin và tương lai của hệ sinh thái Pancake.\n\n&nbsp;\n\n**Tất cả chỉ vì mục đích thông tin tham khảo, bài viết này hoàn toàn không phải là lời khuyên đầu tư\n\n     ** &nbsp;\n\nHy vọng với những thông tin trên sẽ giúp các bạn có nhiều insights thông qua \n\nCapWheel Series Pancake Swap\n\n. Những thông tin về dự án mới nhất sẽ luôn được cập nhật nhanh chóng trên website và các kênh chính thức của \n\nGFI Research\n\n. Các bạn quan tâm đừng quên tham gia vào nhóm cộng đồng của GFI để cùng thảo luận, trao đổi kiến thức và kinh nghiệm với các thành viên khác nhé.\n\n     &nbsp;\n\n&nbsp;\n\n\n\n\n    ~~~metadata \n\n    undefined: undefined\nundefined: undefined\nundefined: undefined\nExcerpt: Pancake nổi bật so với các sàn DEX khác nhờ hệ sinh thái đa dạng, tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn trong mô hình Mint & Burn của CAKE. Tuy nhiên, phần lớn lượng CAKE được Burn vẫn đến từ các hoạt động DEX, trong khi các sản phẩm khác chỉ đóng góp khoảng 11% vào tổng lượng Burn.\n\nĐề xuất loại bỏ veCAKE được đưa ra với mục tiêu kiểm soát nguồn cung hiệu quả hơn, nhưng lại vấp phải tranh cãi gay gắt về tính phi tập trung. Pancake bị nghi ngờ đã có những động thái không minh bạch nhằm giảm sức ép từ các Liquid Wrappers trước khi đề xuất được đưa vào biểu quyết, làm dấy lên nhiều lo ngại trong cộng đồng.\nundefined: undefined\nundefined: undefined\nMeta description: Pancake nổi bật so với các sàn DEX khác nhờ hệ sinh thái đa dạng, tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn trong mô hình Mint & Burn.\n postUrl: capwheel-series-pancakeswap \n ~~~"

    print(check_image(text_llm, image_llm, content))