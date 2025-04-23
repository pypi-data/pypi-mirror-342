"""
This module provides comprehensive evaluation functionality for crypto/Web3 research articles 
following GFI Research style guidelines. It analyzes article structure, content quality,
grammar/language usage, and SEO optimization.

Key features:
- Article structure validation
- Content quality assessment 
- Grammar and style checking
- SEO optimization analysis
- Comprehensive evaluation reporting
"""

from langchain_openai import AzureChatOpenAI

def check_article_structure(llm: AzureChatOpenAI, text: str) -> str:  
    """
    Evaluates the structural organization and formatting of a crypto research article.
    
    Args:
        llm: AzureChatOpenAI instance for text analysis
        text: Article content to evaluate
        
    Returns:
        str: Detailed evaluation report focusing on article structure
        
    Analysis includes:
    - Overall structure (intro, analysis, conclusion)
    - Section organization and flow
    - Heading hierarchy and formatting
    - Content length and distribution
    - Table of contents validation
    """
    prompt = f"""
<EvaluationRequest>
    <Role>
        You are a <strong>cryptocurrency research analyst</strong> with extensive experience in evaluating Web3, DeFi, and blockchain content specifically for investment-oriented audiences. You specialize in assessing both technical accuracy and practical investment value of crypto research.
    </Role>

    <Mission>
        <Overview>
            Your mission is to <strong>thoroughly evaluate a crypto research article</strong> based on GFI Research quality standards, focusing on language quality, technical accuracy, investment perspective clarity, data visualization effectiveness, and actionable insights.
        </Overview>

        <Instructions>
            <Instruction>
                <Title>1. Language & Accessibility Evaluation</Title>
                <Details>
                    <Point>Assess grammar, spelling, and punctuation errors (quote Vietnamese errors with English corrections if applicable).</Point>
                    <Point>Evaluate the balance between technical precision and accessibility for retail investors (not just developers).</Point>
                    <Point>Check if technical jargon is properly introduced and explained when first used.</Point>
                    <Point>Verify paragraph length optimality - flag paragraphs exceeding 150 words that should be broken down for readability.</Point>
                    <Point>Assess if the writing follows the "What-Why-So what" analytical framework rather than simply reporting news.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>2. Structure & Format Evaluation</Title>
                <Details>
                    <Point>Check for clear research-oriented structure: Introduction, Analysis, Assessment, Conclusion.</Point>
                    <Point>Verify presence of a table of contents for articles exceeding 2000 words.</Point>
                    <Point>Assess effectiveness of headings, subheadings, and section transitions in guiding the reader.</Point>
                    <Point>Evaluate the integration of charts, tables and visual elements within the text flow.</Point>
                    <Point>Check for proper use of formatting elements (bullet points, numbered lists, blockquotes) to highlight key points.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>3. Core Content Evaluation</Title>
                <Details>
                    <Point>Assess how effectively the article addresses its stated objective.</Point>
                    <Point>Evaluate whether the introduction clearly establishes context and significance for the chosen Web3/DeFi topic.</Point>
                    <Point>Check for evidence of original analysis beyond summarizing public information.</Point>
                    <Point>Assess if the conclusion provides clear, actionable insights aligned with the preceding analysis.</Point>
                </Details>
                
                <SubInstruction>
                    <Title>3.1 Technical Analysis Quality</Title>
                    <Details>
                        <Point>Evaluate depth of blockchain/Web3 technology explanation (protocols, consensus mechanisms, scaling solutions, etc.).</Point>
                        <Point>Assess the clarity and accuracy of technical aspects specific to projects like LayerZero, EigenLayer, zkSync, or Starknet.</Point>
                        <Point>Check if the project roadmap analysis includes realistic timeline assessments and development milestones.</Point>
                        <Point>Evaluate if technical comparisons with competing solutions are substantive rather than superficial.</Point>
                        <Point>Assess if technical limitations and risks are honestly addressed alongside benefits.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.2 Tokenomics & Valuation Analysis</Title>
                    <Details>
                        <Point>Evaluate the comprehensiveness of token distribution analysis (allocation percentages, holder types).</Point>
                        <Point>Check if token unlock schedules are clearly presented with timeline visualizations.</Point>
                        <Point>Assess if market cap and Fully Diluted Valuation (FDV) calculations are accurate and compared to relevant benchmarks.</Point>
                        <Point>Evaluate if the valuation methodology is explicitly explained and appropriately applied.</Point>
                        <Point>Check if token utility mechanisms and value accrual are critically analyzed beyond marketing claims.</Point>
                        <Point>Assess if sector-specific comparative valuations with similar projects are included.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.3 Investment Strategy & Portfolio Perspective</Title>
                    <Details>
                        <Point>Evaluate if the article provides clear capital allocation recommendations across project categories.</Point>
                        <Point>Check if risk/reward analysis includes specific metrics and realistic scenarios.</Point>
                        <Point>Assess if market timing considerations address both short and long-term horizons.</Point>
                        <Point>Evaluate if portfolio strategy suggestions consider diversification principles.</Point>
                        <Point>Check if potential catalysts and risk factors are identified with anticipated market impacts.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.4 Data Quality & Visualization</Title>
                    <Details>
                        <Point>Evaluate the quality and relevance of on-chain data from sources like Dune Analytics.</Point>
                        <Point>Assess if price charts and technical analysis incorporate meaningful indicators beyond basic patterns.</Point>
                        <Point>Check if TVL metrics, user activity data, and adoption trends are accurately presented.</Point>
                        <Point>Evaluate if charts and graphs effectively visualize key concepts rather than merely decorating the text.</Point>
                        <Point>Assess if data sources are properly attributed and recent (within 7 days for volatile metrics).</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.5 Macro Context Integration</Title>
                    <Details>
                        <Point>Evaluate how effectively regulatory developments (SEC, Fed actions) are linked to project prospects.</Point>
                        <Point>Check if the article connects project-specific analysis to broader crypto market cycles.</Point>
                        <Point>Assess if key events (token unlocks, mainnet launches, hard forks) are analyzed for market impact.</Point>
                        <Point>Evaluate if institutional capital flows and broader financial market trends are considered.</Point>
                    </Details>
                </SubInstruction>
            </Instruction>
        </Instructions>
    </Mission>

    <OutputFormat>
        <Field>Respond in Markdown format.</Field>
        <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
        
        <Section title="Executive Summary">
            <Field>Overall quality assessment: [Concise 2-3 sentence evaluation]</Field>
            <Field>Research Quality Score: x/10</Field>
            <Field>Article Strengths: [3-5 bullet points highlighting strongest aspects]</Field>
            <Field>Priority Improvement Areas: [3-5 bullet points identifying critical gaps]</Field>
            <Field>Word Count: [Total word count]</Field>
        </Section>

        <Section title="Language & Accessibility Evaluation">
            <IssueStructure>
                <CriterionTitle>Grammar & Technical Writing</CriterionTitle>
                <Analysis>Assessment of grammar quality and technical writing clarity</Analysis>
                <ErrorExamples>Specific grammar issues found (quote Vietnamese content if applicable)</ErrorExamples>
                <TechnicalJargonBalance>Evaluation of balance between technical precision and accessibility</TechnicalJargonBalance>
                <ImpressionScore>Language Quality Score: x/10</ImpressionScore>
                <RecommendedImprovements>Specific language enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Readability & Flow</CriterionTitle>
                <ParagraphStructure>Assessment of paragraph length and readability</ParagraphStructure>
                <LongParagraphs>Identification of overlong paragraphs needing division</LongParagraphs>
                <AnalyticalFramework>Evaluation of "What-Why-So what" framework implementation</AnalyticalFramework>
                <RecommendedImprovements>Specific readability enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
        </Section>

        <Section title="Structure & Format Evaluation">
            <IssueStructure>
                <CriterionTitle>Research Structure</CriterionTitle>
                <StructureAssessment>Analysis of the article's overall organization</StructureAssessment>
                <SectionOrganization>Evaluation of Introduction-Analysis-Assessment-Conclusion flow</SectionOrganization>
                <NavigationAids>Assessment of table of contents and heading structure</NavigationAids>
                <ImpressionScore>Structure Quality Score: x/10</ImpressionScore>
                <RecommendedImprovements>Specific structural enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Visual Integration</CriterionTitle>
                <VisualsAssessment>Evaluation of chart and table placement and flow</VisualsAssessment>
                <FormattingEffectiveness>Analysis of formatting element usage (bullets, lists, etc.)</FormattingEffectiveness>
                <RecommendedImprovements>Specific visual integration enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
        </Section>

        <Section title="Core Content Evaluation">
            <IssueStructure>
                <CriterionTitle>Technical Analysis</CriterionTitle>
                <TechnicalAccuracy>Assessment of blockchain/Web3 technology explanation accuracy</TechnicalAccuracy>
                <TechnicalDepth>Evaluation of explanation depth for protocols, mechanisms, etc.</TechnicalDepth>
                <CompetitiveAnalysis>Assessment of technical comparison with competing solutions</CompetitiveAnalysis>
                <RoadmapAnalysis>Evaluation of development milestone and timeline assessment</RoadmapAnalysis>
                <ImpressionScore>Technical Content Score: x/10</ImpressionScore>
                <ContentGaps>Key technical aspects not addressed or insufficiently covered</ContentGaps>
                <RecommendedImprovements>Specific technical content enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Tokenomics & Valuation Analysis</CriterionTitle>
                <TokenomicsCompleteness>Assessment of token distribution and unlock schedule coverage</TokenomicsCompleteness>
                <ValuationMethodology>Evaluation of market cap, FDV, and comparative valuation approach</ValuationMethodology>
                <TokenUtilityAnalysis>Assessment of token utility and value accrual explanation</TokenUtilityAnalysis>
                <ComparativeFramework>Evaluation of sector-specific benchmarking</ComparativeFramework>
                <ImpressionScore>Tokenomics Analysis Score: x/10</ImpressionScore>
                <ContentGaps>Key tokenomics aspects not addressed or insufficiently covered</ContentGaps>
                <RecommendedImprovements>Specific tokenomics analysis enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Investment Strategy</CriterionTitle>
                <AllocationClarity>Assessment of capital allocation recommendation clarity</AllocationClarity>
                <RiskRewardAnalysis>Evaluation of risk/reward scenario analysis</RiskRewardAnalysis>
                <PortfolioContext>Assessment of diversification and portfolio integration guidance</PortfolioContext>
                <CatalystIdentification>Evaluation of catalyst and risk factor analysis</CatalystIdentification>
                <ImpressionScore>Investment Guidance Score: x/10</ImpressionScore>
                <ContentGaps>Key investment aspects not addressed or insufficiently covered</ContentGaps>
                <RecommendedImprovements>Specific investment analysis enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Data Quality & Visualization</CriterionTitle>
                <DataRelevance>Assessment of on-chain and market data relevance</DataRelevance>
                <DataRecency>Evaluation of data freshness and timeliness</DataRecency>
                <VisualizationEffectiveness>Assessment of chart and graph communication effectiveness</VisualizationEffectiveness>
                <SourceAttribution>Evaluation of data source attribution quality</SourceAttribution>
                <ImpressionScore>Data Quality Score: x/10</ImpressionScore>
                <ContentGaps>Key data or visualizations missing or insufficiently developed</ContentGaps>
                <RecommendedImprovements>Specific data presentation enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Macro Context Integration</CriterionTitle>
                <RegulatoryContext>Assessment of regulatory development analysis</RegulatoryContext>
                <MarketCycleAwareness>Evaluation of crypto market cycle integration</MarketCycleAwareness>
                <EventImpactAnalysis>Assessment of key event impact analysis</EventImpactAnalysis>
                <BroaderMarketTrends>Evaluation of institutional capital flow and financial market trend integration</BroaderMarketTrends>
                <ImpressionScore>Macro Context Score: x/10</ImpressionScore>
                <ContentGaps>Key macro factors not addressed or insufficiently covered</ContentGaps>
                <RecommendedImprovements>Specific macro context enhancement suggestions</RecommendedImprovements>
            </IssueStructure>
        </Section>
        
        <Section title="GFI Research Style Alignment">
            <Field>Analytical Depth: [Assessment of depth vs. surface-level reporting]</Field>
            <Field>Personal Perspective: [Evaluation of unique viewpoint integration]</Field>
            <Field>Data-Driven Approach: [Assessment of empirical foundation]</Field>
            <Field>Audience Targeting: [Evaluation of alignment with retail crypto investor needs]</Field>
            <Field>Investment Orientation: [Assessment of actionable investment guidance]</Field>
            <Field>Overall Style Alignment Score: x/10</Field>
        </Section>
        
        <Section title="Priority Improvement Plan">
            <Field>Top 3 highest-impact content improvements: [Ranked list of critical enhancements]</Field>
            <Field>Language & accessibility improvements: [Key language refinements]</Field>
            <Field>Structure & formatting enhancements: [Key structural changes]</Field>
            <Field>Technical analysis strengthening: [Key technical content improvements]</Field>
            <Field>Investment perspective enhancements: [Key investment analysis improvements]</Field>
        </Section>
    </OutputFormat>

    <Content>
        {text}
    </Content>
</EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    response = llm.invoke(prompt)
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error during evaluation: {str(e)}"

def check_content(llm: AzureChatOpenAI, text: str) -> str:
    """
    Performs in-depth evaluation of article content quality and analytical depth.
    
    Args:
        llm: AzureChatOpenAI instance for content analysis
        text: Article content to evaluate
        
    Returns:
        str: Detailed content quality assessment report
        
    Evaluates:
    - Technical accuracy and depth
    - Investment analysis quality
    - Data visualization effectiveness
    - Market analysis comprehensiveness
    - Actionable insights
    """
    prompt = f"""
<EvaluationRequest>
    <Role>
        You are a <strong>specialized crypto content evaluation expert</strong> with extensive knowledge in Web3, DeFi, tokenomics, and blockchain investment analysis, specializing in assessing content that combines technical analysis with practical investment insights for the retail crypto investor community.
    </Role>

    <Mission>
        <Overview>
            Your mission is to <strong>perform a comprehensive evaluation of the article's content quality</strong> based on GFI Research's specific focus areas: project analysis, tokenomics, investment strategies, market data integration, and macro event impact. Your assessment must evaluate both analytical depth and practical investment value while highlighting strengths and weaknesses with specific examples.
        </Overview>

        <Instructions>
            <Instruction>
                <Title>1. Key Insights Evaluation</Title>
                <Details>
                    <Point>Assess whether key insights effectively summarize the most valuable investment-relevant information about the Web3/DeFi project.</Point>
                    <Point>Evaluate how clearly the article identifies the project's unique value proposition within the crypto ecosystem.</Point>
                    <Point>Check if insights provide both technical understanding and investment implications for retail investors.</Point>
                    <Point>Verify that insights go beyond surface-level observations to provide genuinely actionable intelligence.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>2. Project Introduction Assessment</Title>
                <Details>
                    <Point>Analyze how effectively the introduction establishes the project's position in the Web3/DeFi landscape.</Point>
                    <Point>Evaluate whether the project's development roadmap and significant milestones are clearly articulated.</Point>
                    <Point>Assess how well the article explains the problem or opportunity the project addresses in the crypto market.</Point>
                    <Point>Check if the introduction creates interest while maintaining analytical rigor appropriate for crypto investors.</Point>
                    <Point>Evaluate whether the introduction provides context on the project's relation to broader crypto market trends.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>3. Detailed Analysis Assessment</Title>
                <Details>
                    <Point>Verify that technical claims are supported by specific protocol mechanics, code analysis, or authoritative sources.</Point>
                    <Point>Assess the quality and recency of on-chain data and market metrics incorporated into the analysis.</Point>
                    <Point>Evaluate how effectively the article balances technical analysis with investment implications.</Point>
                    <Point>Check for logical consistency throughout the analysis and identify any unfounded assumptions.</Point>
                    <Point>Assess how well complex DeFi/Web3 concepts are explained for retail crypto investors.</Point>
                </Details>
                
                <SubInstruction>
                    <Title>3.1 Core Technology Analysis</Title>
                    <Details>
                        <Point>Assess how thoroughly the article explains the project's blockchain architecture, consensus mechanisms, or layer solutions.</Point>
                        <Point>Evaluate whether the explanation of technical innovations (zkProofs, bridging solutions, etc.) is accurate and accessible.</Point>
                        <Point>Check if the analysis identifies genuine technical advantages rather than repeating marketing claims.</Point>
                        <Point>Assess how effectively the article explains technical trade-offs and design decisions.</Point>
                        <Point>Verify that technical comparisons with alternative projects (e.g., Layer 2s, zkRollups) are fair and comprehensive.</Point>
                        <Point>Evaluate whether performance claims are backed by specific metrics like TPS, finality time, or fee structures.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.2 Tokenomics Analysis</Title>
                    <Details>
                        <Point>Assess how thoroughly the token distribution structure, vesting schedules, and unlock events are analyzed.</Point>
                        <Point>Evaluate whether token utility and value accrual mechanisms are clearly explained.</Point>
                        <Point>Check if the analysis includes circulating supply, maximum supply, and fully diluted valuation metrics.</Point>
                        <Point>Assess how effectively the article compares tokenomics with similar projects in the same segment.</Point>
                        <Point>Verify that token emission schedules and inflation rates are accurately presented with clear methodology.</Point>
                        <Point>Evaluate whether the analysis considers token governance mechanisms and their implications.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.3 Market Position Analysis</Title>
                    <Details>
                        <Point>Assess how thoroughly the competitive landscape analysis identifies key competitors within the specific crypto segment.</Point>
                        <Point>Evaluate whether market adoption metrics (TVL, users, transactions) are supported by current on-chain data.</Point>
                        <Point>Check if the analysis identifies meaningful differentiators that create sustainable competitive advantages.</Point>
                        <Point>Assess how effectively the article analyzes crypto market trends and their implications for the project.</Point>
                        <Point>Verify that growth projections consider realistic adoption curves based on historical crypto patterns.</Point>
                        <Point>Evaluate whether the analysis considers regulatory risks specific to the project's functionality.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.4 Investment Strategy Analysis</Title>
                    <Details>
                        <Point>Assess how thoroughly investment strategies are explained with specific entry/exit considerations.</Point>
                        <Point>Evaluate whether portfolio allocation recommendations are made with clear rationales.</Point>
                        <Point>Check if risk analysis is comprehensive, covering technical, market, regulatory, and execution risks.</Point>
                        <Point>Assess how effectively the article discusses investment time horizons appropriate for the project.</Point>
                        <Point>Verify that the investment thesis is logically connected to the technical and tokenomics analysis.</Point>
                        <Point>Evaluate whether contrarian viewpoints to the investment thesis are fairly presented.</Point>
                        <Point>Check if yield opportunities, staking rewards, or other passive income strategies are analyzed.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.5 On-chain Data & Market Analysis</Title>
                    <Details>
                        <Point>Assess how thoroughly on-chain metrics are integrated to support investment theses.</Point>
                        <Point>Evaluate whether data visualizations effectively communicate trends in price, volume, and usage metrics.</Point>
                        <Point>Check if data sources (Dune Analytics, TradingView, etc.) are properly cited and recent.</Point>
                        <Point>Assess how effectively the article correlates on-chain activity with price action or market behavior.</Point>
                        <Point>Verify that technical indicators or chart patterns are accurately interpreted if included.</Point>
                        <Point>Evaluate whether the analysis includes unique data insights beyond widely available metrics.</Point>
                    </Details>
                </SubInstruction>

                <SubInstruction>
                    <Title>3.6 Macro Events & Catalyst Analysis</Title>
                    <Details>
                        <Point>Assess how thoroughly regulatory developments (SEC, CFTC, etc.) are analyzed for their impact on the project.</Point>
                        <Point>Evaluate whether upcoming technical events (token unlocks, mainnet launches, hard forks) are properly scheduled and assessed.</Point>
                        <Point>Check if the analysis connects traditional finance trends to their crypto market implications.</Point>
                        <Point>Assess how effectively the article discusses macro liquidity conditions affecting crypto capital flows.</Point>
                        <Point>Verify that catalyst timelines are realistic and based on official communications.</Point>
                        <Point>Evaluate whether the article weighs the relative importance of different catalysts.</Point>
                    </Details>
                </SubInstruction>
            </Instruction>

            <Instruction>
                <Title>4. Conclusion Assessment</Title>
                <Details>
                    <Point>Assess how effectively the conclusion synthesizes key findings into actionable investment insights.</Point>
                    <Point>Evaluate whether the article connects project-specific analysis to broader crypto market implications.</Point>
                    <Point>Check if future development milestones are presented with reasonable timelines and catalysts.</Point>
                    <Point>Assess how effectively the conclusion provides specific takeaways for crypto investors.</Point>
                    <Point>Verify that limitations of the analysis and potential blind spots are acknowledged appropriately.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>5. Visual & Data Presentation</Title>
                <Details>
                    <Point>Assess how effectively charts and visualizations enhance understanding of key metrics and trends.</Point>
                    <Point>Evaluate whether complex data is presented in accessible formats appropriate for retail investors.</Point>
                    <Point>Check if visualizations include proper context, labels, and source attributions.</Point>
                    <Point>Assess how well the article balances text analysis with supporting visual evidence.</Point>
                    <Point>Verify that visual elements are properly integrated to support specific analytical points rather than used decoratively.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>6. Accessibility & Educational Value</Title>
                <Details>
                    <Point>Assess how effectively the article explains complex DeFi/Web3 concepts without excessive jargon.</Point>
                    <Point>Evaluate whether technical terms are appropriately defined when introduced.</Point>
                    <Point>Check if the content is structured with clear headings and logical progression.</Point>
                    <Point>Assess how well the article balances depth for experienced crypto users with accessibility for newer investors.</Point>
                    <Point>Verify that the article provides actionable insights regardless of reader's technical background.</Point>
                </Details>
            </Instruction>
        </Instructions>
    </Mission>

    <OutputFormat>
        <Field>Respond in Markdown format.</Field>
        <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
        
        <Section title="Executive Summary">
            <Field>Overall content quality assessment: [Concise 2-3 sentence evaluation]</Field>
            <Field>Content Quality Score: x/10</Field>
            <Field>Content Strengths: [3-5 bullet points highlighting the strongest aspects]</Field>
            <Field>Critical Content Gaps: [3-5 bullet points identifying the most significant deficiencies]</Field>
            <Field>Investment Insight Value: [Brief assessment of how actionable the content is for investors]</Field>
            <Field>Word Count: [Total word count of the article]</Field>
        </Section>

        <Section title="Section-by-Section Content Evaluation">
            <IssueStructure>
                <CriterionTitle>Key Insights</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <ContentGaps>Specific information or perspectives missing from this section</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Project Introduction</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <ContentGaps>Specific information or perspectives missing from this section</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Core Technology Analysis</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <TechnicalAccuracy>Assessment of factual correctness and technical precision</TechnicalAccuracy>
                <ContentGaps>Key technical aspects not sufficiently covered</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Tokenomics Analysis</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <DataQuality>Assessment of tokenomics data accuracy and comprehensiveness</DataQuality>
                <ContentGaps>Missing tokenomics metrics or comparative analyses</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Market Position Analysis</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <CompetitiveAnalysisQuality>Assessment of competitive landscape coverage</CompetitiveAnalysisQuality>
                <ContentGaps>Missing competitive factors or market segments</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Investment Strategy Analysis</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <BalancedPerspective>Assessment of objectivity and balanced presentation</BalancedPerspective>
                <RiskAnalysisQuality>Evaluation of risk assessment comprehensiveness</RiskAnalysisQuality>
                <ContentGaps>Missing investment considerations or scenarios</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>On-chain Data & Market Analysis</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <DataQuality>Assessment of data recency, relevance, and reliability</DataQuality>
                <VisualizationEffectiveness>Evaluation of chart and graph quality and utility</VisualizationEffectiveness>
                <ContentGaps>Missing metrics or analytical approaches</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Macro Events & Catalyst Analysis</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <EventRelevance>Assessment of catalyst selection and impact analysis</EventRelevance>
                <TimelineAccuracy>Evaluation of event scheduling and timeline projections</TimelineAccuracy>
                <ContentGaps>Missing events or catalysts with potential impact</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>

            <IssueStructure>
                <CriterionTitle>Conclusion</CriterionTitle>
                <ContentAssessment>
                    <Strengths>[Bullet points identifying effective elements with specific examples]</Strengths>
                    <Weaknesses>[Bullet points highlighting deficiencies with specific examples]</Weaknesses>
                </ContentAssessment>
                <AnalysisScore>Score: x/10 with brief justification</AnalysisScore>
                <ActionableInsights>Assessment of practical value for investor decision-making</ActionableInsights>
                <ContentGaps>Missing synthesis elements or forward-looking perspectives</ContentGaps>
                <EnhancementRecommendations>Detailed, actionable suggestions for improving content quality</EnhancementRecommendations>
            </IssueStructure>
        </Section>

        <Section title="Visual & Data Presentation Assessment">
            <Field>Overall visual quality: [Assessment of how well charts and graphs enhance the analysis]</Field>
            <Field>Data visualization effectiveness: [Evaluation of how clearly charts communicate key metrics]</Field>
            <Field>Data recency: [Assessment of how current the on-chain and market data are]</Field>
            <Field>Source credibility: [Evaluation of data sources used for analytics]</Field>
            <Field>Enhancement recommendations: [Specific suggestions for improving visual elements]</Field>
        </Section>

        <Section title="Accessibility & Educational Value">
            <Field>Technical clarity: [Evaluation of how effectively complex DeFi/Web3 concepts are explained]</Field>
            <Field>Investor accessibility: [Assessment of content appropriateness for retail crypto investors]</Field>
            <Field>Terminology management: [Evaluation of jargon usage and term explanations]</Field>
            <Field>Knowledge progression: [Assessment of how the article builds understanding from basics to advanced concepts]</Field>
            <Field>Enhancement recommendations: [Specific suggestions to improve educational value]</Field>
        </Section>

        <Section title="Investment Insight Quality">
            <Field>Actionability assessment: [Evaluation of how directly applicable the insights are]</Field>
            <Field>Risk-reward balance: [Assessment of how well the article balances opportunity with risk analysis]</Field>
            <Field>Time horizon clarity: [Evaluation of investment timeframe guidance]</Field>
            <Field>Portfolio context: [Assessment of how the investment fits within broader crypto allocation]</Field>
            <Field>Enhancement recommendations: [Specific suggestions for improving investment value]</Field>
        </Section>

        <Section title="Priority Improvement Plan">
            <Field>Top 5 highest-impact content improvements: [Ranked list of the most critical enhancements]</Field>
            <Field>Missing critical content: [Identification of essential information that should be added]</Field>
            <Field>Content reduction opportunities: [Identification of less valuable content that could be condensed]</Field>
            <Field>Implementation guidance: [Practical advice for implementing the recommended improvements]</Field>
        </Section>
    </OutputFormat>

    <Content>
        {text}
    </Content>
</EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error during evaluation: {str(e)}"

def check_grammar_error(llm: AzureChatOpenAI, text: str) -> str:
    """
    Analyzes grammar, spelling, style and specialized crypto/Web3 terminology usage.
    
    Args:
        llm: AzureChatOpenAI instance for language analysis
        text: Article content to evaluate
        
    Returns:
        str: Detailed language quality assessment report
        
    Checks:
    - Grammar and spelling accuracy
    - Style consistency 
    - Technical terminology usage
    - Writing clarity and accessibility
    - Vietnamese-English translation quality
    """
    prompt = f"""
<EvaluationRequest>
    <Role>
        You are a <strong>language and style expert</strong> specialized in <strong>crypto investment research</strong> with deep knowledge of DeFi, Web3, tokenomics, and blockchain terminology in Vietnamese context.
    </Role>

    <Mission>
        <Overview>
            Your mission is to <strong>evaluate the linguistic quality, readability, and stylistic alignment</strong> of the article with GFI Research's unique analytical style, ensuring it maintains the perfect balance between technical precision and investment accessibility for retail crypto investors.
        </Overview>

        <Instructions>
            <Instruction>
                <Title>1. Check grammar and spelling</Title>
                <Details>
                    <Point>Identify grammatical, spelling, and punctuation errors.</Point>
                    <Point>Ensure sentences are clear, grammatically correct, and unambiguous.</Point>
                    <Point>Quote the erroneous sentences in Vietnamese and suggest corrections in English.</Point>
                    <Point>Check for consistency in crypto-specific terminology translations.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>2. Evaluate GFI Research style alignment</Title>
                <Details>
                    <Point>Assess adherence to GFI Research's analytical style: in-depth analysis (What-Why-So what structure).</Point>
                    <Point>Check for presence of personal assessment or viewpoints alongside factual analysis.</Point>
                    <Point>Ensure the content has a clear investment-oriented angle rather than merely reporting news.</Point>
                    <Point>Verify the article maintains a professional but accessible tone appropriate for retail crypto investors.</Point>
                    <Point>Check for proper structure: Introduction, Analysis, Assessment, and Conclusion sections.</Point>
                    <Point>Verify presence of a table of contents for longer articles.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>3. Check structure and formatting</Title>
                <Details>
                    <Point>Check article length, ensuring substantial content of at least 2500 words for comprehensive topics.</Point>
                    <Point>Flag paragraphs exceeding 150 words and suggest logical splitting points.</Point>
                    <Point>Identify paragraphs that are too short (1-2 sentences) that could be expanded.</Point>
                    <Point>Assess the use of formatting elements: headers, subheaders, bullet points, and numbered lists.</Point>
                    <Point>Check for proper visual separation between different analysis sections.</Point>
                    <Point>Verify that chart and data references are properly integrated with surrounding text.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>4. Evaluate technical language balance</Title>
                <Details>
                    <Point>Assess the balance between technical DeFi/crypto terminology and explanatory content.</Point>
                    <Point>Check if complex concepts (zkProofs, MEV, liquidity fragmentation, etc.) are properly explained.</Point>
                    <Point>Identify overuse of technical jargon that might alienate retail investors.</Point>
                    <Point>Verify that technical terms unique to a specific protocol are introduced with explanations.</Point>
                    <Point>Assess consistent use of crypto metrics (TVL, FDV, APY, etc.) with proper context.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>5. Evaluate investment language quality</Title>
                <Details>
                    <Point>Check for clear articulation of investment theses, risk factors, and potential catalysts.</Point>
                    <Point>Assess precision in discussing financial metrics, tokenomics, and market dynamics.</Point>
                    <Point>Verify responsible use of language regarding investment projections and forward-looking statements.</Point>
                    <Point>Check for balanced presentation of both bullish and bearish perspectives.</Point>
                    <Point>Identify any vague or imprecise language in sections discussing potential returns or risks.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>6. Check data presentation language</Title>
                <Details>
                    <Point>Verify that chart descriptions and data interpretations are clear and accurate.</Point>
                    <Point>Check if numerical data is presented consistently with appropriate units and context.</Point>
                    <Point>Assess clarity of language used to explain trends, patterns, or anomalies in data.</Point>
                    <Point>Verify proper citation of data sources with dates.</Point>
                    <Point>Check for clear explanations of any metrics or calculations unique to the analysis.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>7. Check word choice and repetition</Title>
                <Details>
                    <Point>Identify unnecessary repetition of words or phrases (excluding important crypto terminology).</Point>
                    <Point>Suggest synonyms or alternative expressions to improve readability and engagement.</Point>
                    <Point>Check for consistent use of key terms throughout the article.</Point>
                    <Point>Identify overused transition phrases or analytical expressions.</Point>
                </Details>
            </Instruction>

            <Instruction>
                <Title>8. Evaluate coherence and flow</Title>
                <Details>
                    <Point>Assess logical connections between paragraphs and sections.</Point>
                    <Point>Check if the article progresses logically from introduction to conclusion.</Point>
                    <Point>Verify smooth transitions between technical analysis and investment implications.</Point>
                    <Point>Ensure clear connections between data presented and conclusions drawn.</Point>
                    <Point>Check if main arguments are developed consistently throughout the article.</Point>
                </Details>
            </Instruction>
        </Instructions>
    </Mission>

    <OutputFormat>
        <Field>Respond in Markdown format.</Field>
        <Field>Respond in English. Only quoted content should remain in Vietnamese.</Field>
        
        <Section title="Overview">
            <Field>Overall evaluation of language and style quality: [Brief summary]</Field>
            <Field>GFI Research style alignment score: x/10</Field>
            <Field>Language quality score: x/10</Field>
            <Field>Word count: [Insert actual word count]</Field>
            <Field>Key strengths: [List 3-4 strongest style elements]</Field>
            <Field>Priority improvement areas: [List 3-4 most critical style issues]</Field>
        </Section>

        <Section title="GFI Research Style Alignment">
            <Analysis>Assessment of how well the article matches GFI Research's analytical style</Analysis>
            <StrengthsListings>Notable examples where the article successfully demonstrates the expected style</StrengthsListings>
            <WeaknessListings>Areas where the article deviates from the expected style</WeaknessListings>
            <RecommendedImprovements>Specific suggestions to better align with GFI Research style</RecommendedImprovements>
        </Section>

        <Section title="Grammar and Language Quality">
            <IssueStructure>
                <CriterionTitle>Grammar and Spelling</CriterionTitle>
                <Analysis>Overall assessment of grammatical quality</Analysis>
                <DetailedIssues>List specific errors with quotes and suggested corrections</DetailedIssues>
                <TerminologyConsistency>Assessment of crypto terminology consistency</TerminologyConsistency>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Technical Language Balance</CriterionTitle>
                <Analysis>Assessment of balance between technical precision and accessibility</Analysis>
                <OverSpecializedTerms>List of technical terms that need better explanation</OverSpecializedTerms>
                <TermExplanationQuality>Evaluation of how well complex concepts are explained</TermExplanationQuality>
                <ImproveRecommendations>Suggestions for better balancing technical content</ImproveRecommendations>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Investment Language Precision</CriterionTitle>
                <Analysis>Assessment of language clarity when discussing investment concepts</Analysis>
                <ProblemAreas>Identification of vague or imprecise investment language</ProblemAreas>
                <BalancedPerspective>Evaluation of balanced presentation of bull/bear cases</BalancedPerspective>
                <ImproveRecommendations>Suggestions for more precise investment language</ImproveRecommendations>
            </IssueStructure>
        </Section>

        <Section title="Structure and Formatting">
            <IssueStructure>
                <CriterionTitle>Document Structure</CriterionTitle>
                <Analysis>Assessment of overall structure and section organization</Analysis>
                <StructuralGaps>Identification of missing key sections</StructuralGaps>
                <ImproveRecommendations>Suggestions for structural improvements</ImproveRecommendations>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Paragraph Length and Balance</CriterionTitle>
                <Analysis>Assessment of paragraph structure throughout the document</Analysis>
                <LongParagraphs>List paragraphs exceeding 150 words with suggestions for breaking them up</LongParagraphs>
                <ShortParagraphs>List paragraphs that are too short with suggestions for expansion</ShortParagraphs>
                <ImproveRecommendations>Suggestions for better paragraph structuring</ImproveRecommendations>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Formatting Elements</CriterionTitle>
                <Analysis>Assessment of headings, lists, and visual elements usage</Analysis>
                <FormattingGaps>Areas where better formatting would improve readability</FormattingGaps>
                <ImproveRecommendations>Specific formatting improvement suggestions</ImproveRecommendations>
            </IssueStructure>
        </Section>

        <Section title="Content Flow and Coherence">
            <IssueStructure>
                <CriterionTitle>Logical Progression</CriterionTitle>
                <Analysis>Assessment of idea flow and logical development</Analysis>
                <CoherenceIssues>Identification of logic breaks or weak transitions</CoherenceIssues>
                <ImproveRecommendations>Suggestions for improving argument flow</ImproveRecommendations>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Data Integration</CriterionTitle>
                <Analysis>Assessment of how well data and charts are incorporated into the narrative</Analysis>
                <IntegrationIssues>Identification of disconnects between data and text</IntegrationIssues>
                <ImproveRecommendations>Suggestions for better data-text integration</ImproveRecommendations>
            </IssueStructure>
            
            <IssueStructure>
                <CriterionTitle>Word Choice and Repetition</CriterionTitle>
                <Analysis>Assessment of vocabulary diversity and appropriate repetition</Analysis>
                <RepetitiveElements>List of overused words or phrases with alternatives</RepetitiveElements>
                <ImproveRecommendations>Suggestions for more varied language</ImproveRecommendations>
            </IssueStructure>
        </Section>

        <Section title="Priority Improvement Recommendations">
            <Field>Top 5 language and style improvements: [Ranked list of the most impactful changes]</Field>
            <Field>Implementation suggestions: [Practical guidance for applying the recommendations]</Field>
            <Field>Style enhancement resources: [Suggested reference materials or examples for improvement]</Field>
        </Section>
    </OutputFormat>

    <Content>
        {text}
    </Content>
</EvaluationRequest>
    """
    # Invoke the LLM with the evaluation criteria and content

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error during evaluation: {str(e)}"

def check_seo(llm: AzureChatOpenAI, text: str, metadata: str = None) -> str:
    """
    Performs comprehensive SEO evaluation for crypto research articles.
    
    Args:
        llm: AzureChatOpenAI instance for SEO analysis
        text: Article content to evaluate
        metadata: Optional metadata about the article
        
    Returns:
        str: Detailed SEO optimization report
        
    Analyzes:
    - Keyword optimization
    - Link structure
    - URL optimization
    - Content structure
    - Technical SEO elements
    """
    prompt = f"""
    <CryptoResearchSEOEvaluation>
        <Role>
            You are a specialized <strong>SEO expert</strong> with deep knowledge of Web3, DeFi, and cryptocurrency content optimization. 
            You understand both technical blockchain concepts and SEO best practices for crypto research content.
            You are especially skilled at evaluating Vietnamese cryptocurrency content and adapting SEO principles for the Vietnamese market.
        </Role>

        <Mission>
            <Overview>
                Evaluate this cryptocurrency research article following GFI Research style guidelines for comprehensive SEO optimization.
                Focus on making the content discoverable, authoritative, and valuable for crypto investors and enthusiasts.
                Generate optimized URL suggestions using Vietnamese words without diacritics.
            </Overview>

            <ContentContext>
                <Focus>Web3 & DeFi project analysis, tokenomics, investment strategies, market data, and macro events</Focus>
                <Style>Analytical, data-driven, clear structure, professional but accessible language, investment-oriented</Style>
                <Audience>Vietnamese crypto investors (both retail and institutional), DeFi users, blockchain enthusiasts</Audience>
            </ContentContext>
        </Mission>

        <EvaluationCriteria>
            <Section title="1. Keyword Optimization">
                <Criterion>
                    <Title>Project & Token Keywords</Title>
                    <Description>
                        <Point>Check if primary project keywords (e.g., protocol name, token ticker) appear in title, H1, meta description, and first 100 words</Point>
                        <Point>Analyze keyword density (optimal: 1-2% for primary keywords)</Point>
                        <Point>Check for blockchain-specific terminology appropriately distributed</Point>
                        <Point>Evaluate use of both English crypto terms and Vietnamese equivalents where appropriate</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Crypto Category Keywords</Title>
                    <Description>
                        <Point>Evaluate usage of category terms (DeFi, Layer 2, zkRollup, etc.) relevant to the project</Point>
                        <Point>Check for appropriate synonyms and variations in both English and Vietnamese</Point>
                        <Point>Verify consistent usage of technical terms throughout the article</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Research & Analysis Keywords</Title>
                    <Description>
                        <Point>Check for analytical terms (tokenomics, valuation, market analysis, etc.)</Point>
                        <Point>Evaluate distribution of investment-related keywords (risk/reward, allocation, portfolio, etc.)</Point>
                        <Point>Verify use of market-specific terminology relevant to current crypto trends</Point>
                    </Description>
                </Criterion>
            </Section>

            <Section title="2. Link Structure">
                <Criterion>
                    <Title>Internal Research Links</Title>
                    <Description>
                        <Point>Check for links to related research content (previous analysis, token reports, etc.)</Point>
                        <Point>Evaluate references to other projects in the same category</Point>
                        <Point>Verify if there are links to GFI Research tools or dashboards</Point>
                        <Point>Check if internal links use descriptive anchor text in Vietnamese</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>External Authority Links</Title>
                    <Description>
                        <Point>Check for links to project documentation, official announcements, GitHub repos</Point>
                        <Point>Verify references to trusted data sources (Dune Analytics, TradingView, CoinGecko, etc.)</Point>
                        <Point>Evaluate links to relevant blockchain explorers or protocol dashboards</Point>
                        <Point>Check for links to Vietnamese crypto communities or resources where relevant</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Link Quality & Anchors</Title>
                    <Description>
                        <Point>Evaluate anchor text relevance and descriptiveness</Point>
                        <Point>Check if links provide genuine value vs. appearing promotional</Point>
                        <Point>Verify appropriate use of nofollow for exchange links or sponsored content</Point>
                        <Point>Ensure anchor text is natural in Vietnamese context while including relevant keywords</Point>
                    </Description>
                </Criterion>
            </Section>

            <Section title="3. URL Optimization">
                <Criterion>
                    <Title>URL Structure & Keywords</Title>
                    <Description>
                        <Point>Evaluate if the current URL (if provided) follows SEO best practices</Point>
                        <Point>Check if URL contains main keywords related to the article topic</Point>
                        <Point>Verify URL uses Vietnamese words without diacritics (as per GFI Research standard)</Point>
                        <Point>Analyze if URL accurately reflects article content while remaining readable</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>URL Length & Formatting</Title>
                    <Description>
                        <Point>Check if URL follows proper hyphenation format (words separated by hyphens)</Point>
                        <Point>Verify URL avoids unnecessary words (articles, prepositions) while maintaining meaning</Point>
                        <Point>Ensure URL contains no more than 25 words and preferably under 150 characters</Point>
                        <Point>Check that URL doesn't contain special characters, underscores, or spaces</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>URL Consistency & Branding</Title>
                    <Description>
                        <Point>Verify URL follows GFI Research URL pattern: https://gfiresearch.net/post/[slug]</Point>
                        <Point>Check if URL aligns with similar articles on the platform for consistency</Point>
                        <Point>Evaluate if URL represents the GFI Research brand appropriately</Point>
                    </Description>
                </Criterion>
            </Section>

            <Section title="4. Content Structure & Readability">
                <Criterion>
                    <Title>Research-Appropriate Structure</Title>
                    <Description>
                        <Point>Verify presence of clear sections (Introduction, Analysis, Insights, Conclusion)</Point>
                        <Point>Check for table of contents in longer articles</Point>
                        <Point>Evaluate H2/H3 hierarchy and keyword inclusion in headings</Point>
                        <Point>Verify logical progression of ideas suited for Vietnamese readers</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Data Visualization</Title>
                    <Description>
                        <Point>Check for charts, graphs, and data visualizations with proper alt text</Point>
                        <Point>Verify presence of tokenomics diagrams, price charts, or other relevant visuals</Point>
                        <Point>Evaluate image optimization and descriptive naming</Point>
                        <Point>Check if visualizations have Vietnamese labels or explanations where needed</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Crypto-Specific Formatting</Title>
                    <Description>
                        <Point>Check for proper formatting of token symbols, addresses, and blockchain terms</Point>
                        <Point>Verify use of tables for comparison data (market caps, TVL, etc.)</Point>
                        <Point>Evaluate use of code blocks for smart contract examples if applicable</Point>
                        <Point>Check if technical terms are explained appropriately for Vietnamese audience</Point>
                    </Description>
                </Criterion>
            </Section>

            <Section title="5. Technical SEO Elements">
                <Criterion>
                    <Title>Meta Elements</Title>
                    <Description>
                        <Point>Check title tag optimization with main project/token name (under 60 chars)</Point>
                        <Point>Verify meta description includes value proposition and keywords (under 160 chars)</Point>
                        <Point>Evaluate URL structure (should include main project/token name)</Point>
                        <Point>Check if meta elements are optimized for Vietnamese search patterns</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Schema & Structured Data</Title>
                    <Description>
                        <Point>Check for Article schema implementation</Point>
                        <Point>Verify appropriate dates (published, modified) for timely crypto content</Point>
                        <Point>Evaluate author attribution and expertise signals</Point>
                        <Point>Check for any Vietnam-specific structured data if applicable</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Social Sharing Optimization</Title>
                    <Description>
                        <Point>Check for Open Graph tags with crypto-specific thumbnails</Point>
                        <Point>Verify Twitter card implementation</Point>
                        <Point>Evaluate social-ready headlines and descriptions</Point>
                        <Point>Check optimization for popular Vietnamese social platforms</Point>
                    </Description>
                </Criterion>
            </Section>

            <Section title="6. Crypto Research Value Signals">
                <Criterion>
                    <Title>Expertise & Authority</Title>
                    <Description>
                        <Point>Evaluate depth of technical explanation (shows protocol understanding)</Point>
                        <Point>Check for unique insights not available in basic documentation</Point>
                        <Point>Verify reference to on-chain data and research methodology</Point>
                        <Point>Assess localization of global crypto concepts for Vietnamese market</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Investment Perspective</Title>
                    <Description>
                        <Point>Check for risk/reward analysis balanced with technical assessment</Point>
                        <Point>Verify comparison to similar projects or market benchmarks</Point>
                        <Point>Evaluate inclusion of potential catalysts or risk factors</Point>
                        <Point>Check if content addresses Vietnamese investor concerns specifically</Point>
                    </Description>
                </Criterion>
                
                <Criterion>
                    <Title>Content Freshness</Title>
                    <Description>
                        <Point>Check for recent data points and market updates</Point>
                        <Point>Verify reference to current development stage or roadmap status</Point>
                        <Point>Evaluate timeliness regarding token events (unlocks, emissions changes)</Point>
                        <Point>Check if content references recent events affecting Vietnamese crypto market</Point>
                    </Description>
                </Criterion>
            </Section>
        </EvaluationCriteria>

        <OutputFormat>
            <Section title="Executive Summary">
                <Field>Overall SEO Quality Score: X/10</Field>
                <Field>Key Strengths: [Top 3 strengths]</Field>
                <Field>Priority Improvements: [Top 3 improvements]</Field>
            </Section>

            <Section title="URL Optimization">
                <Field>Current URL Assessment: [If provided in metadata]</Field>
                <Field>Top 5 Suggested URLs:</Field>
                <URLSuggestions>
                    <URL>https://gfiresearch.net/post/[suggested-slug-1]</URL>
                    <URL>https://gfiresearch.net/post/[suggested-slug-2]</URL>
                    <URL>https://gfiresearch.net/post/[suggested-slug-3]</URL>
                    <URL>https://gfiresearch.net/post/[suggested-slug-4]</URL>
                    <URL>https://gfiresearch.net/post/[suggested-slug-5]</URL>
                </URLSuggestions>
                <URLReasoning>Explanation of URL optimization choices...</URLReasoning>
            </Section>

            <Section title="Detailed SEO Evaluation">
                <CriterionEvaluation>
                    <Category>Keyword Optimization</Category>
                    <Score>X/10</Score>
                    <Strengths>...</Strengths>
                    <Issues>...</Issues>
                    <Recommendations>...</Recommendations>
                </CriterionEvaluation>
                
                <CriterionEvaluation>
                    <Category>Link Structure</Category>
                    <Score>X/10</Score>
                    <Strengths>...</Strengths>
                    <Issues>...</Issues>
                    <Recommendations>...</Recommendations>
                </CriterionEvaluation>
                
                <CriterionEvaluation>
                    <Category>Content Structure & Readability</Category>
                    <Score>X/10</Score>
                    <Strengths>...</Strengths>
                    <Issues>...</Issues>
                    <Recommendations>...</Recommendations>
                </CriterionEvaluation>
                
                <CriterionEvaluation>
                    <Category>Technical SEO Elements</Category>
                    <Score>X/10</Score>
                    <Strengths>...</Strengths>
                    <Issues>...</Issues>
                    <Recommendations>...</Recommendations>
                </CriterionEvaluation>
                
                <CriterionEvaluation>
                    <Category>Crypto Research Value Signals</Category>
                    <Score>X/10</Score>
                    <Strengths>...</Strengths>
                    <Issues>...</Issues>
                    <Recommendations>...</Recommendations>
                </CriterionEvaluation>
            </Section>

            <Section title="Actionable Optimization Plan">
                <PriorityAction>
                    <Title>Immediate Actions (High Impact)</Title>
                    <Steps>
                        <Step>...</Step>
                        <Step>...</Step>
                        <Step>...</Step>
                    </Steps>
                </PriorityAction>
                
                <PriorityAction>
                    <Title>Secondary Improvements</Title>
                    <Steps>
                        <Step>...</Step>
                        <Step>...</Step>
                        <Step>...</Step>
                    </Steps>
                </PriorityAction>
                
                <PriorityAction>
                    <Title>Advanced Optimizations</Title>
                    <Steps>
                        <Step>...</Step>
                        <Step>...</Step>
                        <Step>...</Step>
                    </Steps>
                </PriorityAction>
            </Section>
        </OutputFormat>

        <Content>
            {text}
        </Content>
        
        <Metadata>
            {metadata if metadata else "No metadata provided."}
        </Metadata>
    </CryptoResearchSEOEvaluation>
    """

    # Invoke the LLM with the comprehensive evaluation prompt
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error during evaluation: {str(e)}"

def check_text(llm: AzureChatOpenAI, text: str) -> str:
    """
    Master function that performs comprehensive article evaluation by combining
    all individual analysis components.
    
    Args:
        llm: AzureChatOpenAI instance for text analysis
        text: Article content to evaluate
        
    Returns:
        str: Complete evaluation report including:
        - Executive summary
        - Structure analysis
        - Content quality assessment 
        - Language evaluation
        - SEO optimization report
        - Improvement recommendations
        
    The function coordinates multiple specialized evaluations and combines
    their results into a single, well-organized report in Vietnamese.
    """
    # Collect all individual evaluation results asynchronously if possible
    # If async not available, we'll call them sequentially

    # Add input validation
    if not text or not isinstance(text, str):
        return "Invalid input: Text must be a non-empty string"
    if not llm:
        return "Invalid input: Language model required"

    blog = text.split("~~~metadata")
    text = blog[0]
    metadata = blog[1][:-3]

    try:
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        async def run_evaluations():
            with ThreadPoolExecutor(max_workers=4) as executor:
                seo_task = executor.submit(check_seo, llm, text, metadata)
                structure_task = executor.submit(check_article_structure, llm, text)
                content_task = executor.submit(check_content, llm, text)
                grammar_task = executor.submit(check_grammar_error, llm, text)
                
                # Wait for all tasks to complete
                # This is more efficient than sequential execution
                check_seo_result = seo_task.result()
                check_article_structure_result = structure_task.result()
                check_content_result = content_task.result()
                check_grammar_error_result = grammar_task.result()
                
                return check_seo_result, check_article_structure_result, check_content_result, check_grammar_error_result
        
        # Run evaluations concurrently
        check_seo_result, check_article_structure_result, check_content_result, check_grammar_error_result = asyncio.run(run_evaluations())
        
    except (ImportError, RuntimeError):
        # Fallback to sequential execution if async is not available
        check_seo_result = check_seo(llm, text, metadata)
        check_article_structure_result = check_article_structure(llm, text)
        check_content_result = check_content(llm, text)
        check_grammar_error_result = check_grammar_error(llm, text)

    # Combine all results into a structured format
    combined_result = f"""
# Kết quả đánh giá cấu trúc bài viết:
{check_article_structure_result}

# Kết quả đánh giá nội dung bài viết:
{check_content_result}

# Kết quả đánh giá ngữ pháp, chính tả, phong cách và độ dài:
{check_grammar_error_result}

# Kết quả đánh giá SEO:
{check_seo_result}
    """
    
    # Format the detailed report with proper Markdown and translate to Vietnamese
    formatting_prompt = """
    <FormattingRequest>
        <Role>
            You are an expert editor specializing in technical documentation and SEO analysis.
        </Role>
        
        <Task>
            Format the following evaluation results into a well-structured and visually appealing Markdown document.
            Translate all content into Vietnamese while preserving technical terms.
            The output should be clean, professional, and easy to navigate.
        </Task>
        
        <Guidelines>
            <Guideline>Use clear hierarchy with headings (##, ###) and subheadings</Guideline>
            <Guideline>Transform lists into properly formatted bullet points or numbered lists</Guideline>
            <Guideline>Use tables where appropriate for comparative data</Guideline>
            <Guideline>Use bold and italic formatting to highlight important information</Guideline>
            <Guideline>Preserve all technical terms, scores, and metrics</Guideline>
            <Guideline>Maintain a consistent style throughout the document</Guideline>
            <Guideline>Return only the formatted markdown without code blocks or explanations</Guideline>
        </Guidelines>
        
        <Content>
        {result}
        </Content>
    </FormattingRequest>
    """
    
    detailed_result = llm.invoke(formatting_prompt.format(result=combined_result)).content

    def remove_markdown_code_blocks(text):
        # Strip markdown code blocks if present
        if "```markdown" in text:
            text = text.split("```markdown", 1)[1]
        if "```" in text:
            text = text.split("```", 1)[0]
        return text
    
    detailed_result = remove_markdown_code_blocks(detailed_result)
    
    # Create summary with scores and key points
    summary_prompt = """
    <SummaryRequest>
        <Role>
            You are an expert SEO analyst and content strategist specializing in cryptocurrency content.
        </Role>
        
        <Task>
            Create a concise executive summary of the evaluation results with the following components:
            1. Overall score (average of all section scores)
            2. Key strengths (3-5 points)
            3. Priority improvements (3-5 points)
            4. Section-by-section scores with brief 1-2 sentence summary
            
            The summary should be in Vietnamese and formatted in Markdown.
        </Task>
        
        <Guidelines>
            <Guideline>Be concise but informative - executive summary should be no more than 20-25 lines</Guideline>
            <Guideline>Extract actual scores from the evaluation if available, or assign reasonable scores (0-10)</Guideline>
            <Guideline>Focus on actionable insights rather than general observations</Guideline>
            <Guideline>Prioritize items that would have the biggest impact on article performance</Guideline>
            <Guideline>Return only the formatted summary without code blocks or explanations</Guideline>
        </Guidelines>
        
        <Content>
        {result}
        </Content>
    </SummaryRequest>
    """
    
    summary_result = llm.invoke(summary_prompt.format(result=combined_result)).content
    
    summary_result = remove_markdown_code_blocks(summary_result)
    
    # Generate supplementary content improvement suggestions
    improvement_prompt = """
    <ImprovementRequest>
        <Role>
            You are an expert crypto content strategist specializing in Vietnamese market research.
        </Role>
        
        <Task>
            Based on the evaluation results, provide 3-5 specific content improvement suggestions 
            that would significantly enhance the article's quality and SEO performance.
            Focus on concrete examples and actionable advice.
        </Task>
        
        <Guidelines>
            <Guideline>Suggest specific sections or paragraphs that could be enhanced</Guideline>
            <Guideline>Provide examples of better phrasing or structure when possible</Guideline>
            <Guideline>Recommend additional content elements that would improve completeness</Guideline>
            <Guideline>Suggest SEO enhancements that align with Vietnamese search patterns</Guideline>
            <Guideline>Return suggestions in Vietnamese, formatted in Markdown</Guideline>
        </Guidelines>
        
        <Content>
        {result}
        </Content>
        
        <ArticleText>
        {text}
        </ArticleText>
    </ImprovementRequest>
    """
    
    improvement_suggestions = llm.invoke(improvement_prompt.format(result=combined_result, text=text)).content
    
    # Strip markdown code blocks if present
    improvement_suggestions = remove_markdown_code_blocks(improvement_suggestions)
    
    # Add improvement suggestions to the summary
    summary_result += "\n\n## Đề xuất cải thiện\n" + improvement_suggestions
    
    # Combine summary and detailed report
    final_result = f"""
# 📝 TÓM TẮT ĐÁNH GIÁ
{summary_result}

---

# 📋 BÁO CÁO CHI TIẾT
{detailed_result}
"""
    
    return final_result

if __name__ == "__main__":
    import os
    from langchain_openai import AzureChatOpenAI
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()

    # Initialize Azure OpenAI API with credentials and configuration
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini",
        api_version="2024-12-01-preview",
    )

    text = "![Cover Image](https://statics.gemxresearch.com/images/2025/04/11/154715/capwheel-series-pancake-swap.jpg)\n\n# CapWheel Series: PancakeSwap và token $CAKE\n\n **CapWheel Series** là chuỗi bài viết chuyên sâu [phân tích](https://gfiresearch.net/analysis) cách các dự án thiết kế mô hình Tokenomics và sản phẩm để khai thác giá trị cho token của họ. Mục tiêu của series này là cung cấp cái nhìn sâu sắc về giá trị nội tại của token, giúp đánh giá tiềm năng dài hạn của các dự án, thay vì chỉ chú trọng vào biến động ngắn hạn trên thị trường. CapWheel Series tập trung vào việc các dự án xây dựng cơ chế tích lũy giá trị qua các mô hình Tokenomics, thay vì phụ thuộc vào các yếu tố bên ngoài như tình hình thị trường chung hay sự tác động của các yếu tố đầu cơ. \n ## Điểm nổi bật\n\n- Pancake nổi bật so với các sàn DEX khác nhờ hệ sinh thái đa dạng, tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn trong mô hình Mint &amp; Burn của CAKE. Tuy nhiên, phần lớn lượng CAKE được Burn vẫn đến từ các hoạt động DEX, trong khi các sản phẩm khác chỉ đóng góp khoảng 11% vào tổng lượng Burn.\n\n\n- Đề xuất loại bỏ veCAKE được đưa ra với mục tiêu kiểm soát nguồn cung hiệu quả hơn, nhưng lại vấp phải tranh cãi gay gắt về tính phi tập trung. Pancake bị nghi ngờ đã có những động thái không minh bạch nhằm giảm sức ép từ các Liquid Wrappers trước khi đề xuất được đưa vào biểu quyết, làm dấy lên nhiều lo ngại trong cộng đồng.\n\n\n \n ## Tổng quan về PancakeSwap\n\nPancakeSwap hiện là sàn giao dịch phi tập trung (DEX) hàng đầu trên BNB Smart Chain, ghi dấu ấn với khối lượng giao dịch vượt trội, khẳng định vị thế tiên phong trong thị trường tài chính phi tập trung (DeFi). Với sự đổi mới không ngừng, PancakeSwap mang đến một hệ sinh thái đa dạng, tối ưu hóa trải nghiệm cho người dùng, nhà phát triển và nhà cung cấp thanh khoản.\n\nCác \n\nsản phẩm \n\ntrong hệ sinh thái PancakeSwap\n\nPancakeSwap cung cấp một loạt sản phẩm tiên tiến, được thiết kế để đáp ứng nhu cầu đa dạng của cộng đồng DeFi. Dưới đây là những điểm nhấn quan trọng:\n\nAMM Swap\n\nKế thừa từ Uniswap, PancakeSwap không chỉ tái hiện đầy đủ các tính năng cốt lõi mà còn nâng tầm với phiên bản V4, mang đến những cải tiến đột phá:\n\n- Hooks: Các hợp đồng thông minh bên ngoài cho phép tùy chỉnh linh hoạt các hồ thanh khoản, hỗ trợ phí động (thấp đến 0%), công cụ giao dịch nâng cao (lệnh giới hạn, chốt lời, TWAMM, hoàn phí), và tạo doanh thu cho nhà phát triển, thúc đẩy đổi mới.\n\n\n- Đa dạng Liquidity Pool tích hợp liền mạch với HOOKS như Concentrated Liquidity Automated Market Maker (CLAMM), Liquidity Book AMM (LBAMM) hay các Liquidity Pool có thiết kế mở, sẵn sàng cho các mô hình AMM mới, đáp ứng nhu cầu thị trường.\n\n\n- Donate: Khuyến khích nhà cung cấp thanh khoản trong phạm vi giá phù hợp, tăng lợi nhuận và sự tham gia.\n\n\n- Singleton: Gộp tất cả hồ thanh khoản vào một hợp đồng, giảm 99% chi phí tạo hồ và tối ưu gas cho giao dịch đa bước.\n\n\n- Flash Accounting: Tối ưu gas bằng cách tính toán số dư ròng và thanh toán tập trung, giảm chi phí so với mô hình cũ.\n\n\n- ERC-6909: Chuẩn đa token, quản lý token thay thế và không thay thế trong một hợp đồng, tăng hiệu quả, giảm chi phí.\n\n\n- Token Gas Gốc: Hỗ trợ giao dịch với token gas gốc, giảm chi phí và cải thiện trải nghiệm người dùng.\n\n\n- Mã Nguồn Mở: Khuyến khích nhà phát triển đổi mới và hợp tác thông qua giấy phép mở.\n\n\n- Chương trình Nhà phát triển: Quỹ 500.000 USD hỗ trợ chiến dịch tăng trưởng, hackathon, đại sứ phát triển, và tài trợ CAKE, thúc đẩy sáng tạo cộng đồng.\n\n\nEarn\n\n**Add LP &amp; Farming**Tương tự như các AMM Dex khác, người dùng có thể add liquid vào các liquidity pools ở trong Pancake và stake LP để farm ra CAKE từ lượng Emission.\n\n![](https://statics.gemxresearch.com/images/2025/04/11/154948/ADD-LP.png)  **Staking &amp; Syrup Pool**Syrup Pool là một sản phẩm staking của PancakeSwap, cho phép người dùng khóa CAKE hoặc các token khác để nhận phần thưởng dưới dạng CAKE hoặc token từ các dự án đối tác. Đây là cách đơn giản để kiếm lợi nhuận thụ động, đồng thời hỗ trợ hệ sinh thái PancakeSwap. Có hai loại pool chính:\n\n- CAKE Pool: Stake CAKE để nhận CAKE hoặc iCAKE (dùng cho IFO), chia thành Flexible Staking (rút bất kỳ lúc nào, APR thấp hơn) và Fixed-Term Staking (khóa cố định 1-52 tuần, APR cao hơn, tự động gia hạn trừ khi rút).\n\n\n- Non-CAKE Pool: Stake token từ dự án đối tác để nhận phần thưởng là token dự án đó hoặc CAKE, thường có thời hạn cố định.\n\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152622/Syrup Pool.png)  **IFO**Initial Farm Offering (IFO) của PancakeSwap là một cơ hội độc đáo để người dùng tiếp cận sớm các token mới, tương tự IDO nhưng được thiết kế riêng với sự tham gia thông qua CAKE, mang đến tiềm năng lợi nhuận hấp dẫn.\n\nĐể tham gia, người dùng cần khóa CAKE trong để nhận veCAKE, từ đó tạo ra iCAKE – chỉ số quyết định hạn mức tham gia IFO, với số lượng và thời gian khóa càng lớn\n\n thì iCAKE càng cao, mở rộng cơ hội trong Public Sale. Ngoài ra, cần tạo NFT Profile với một khoản phí nhỏ bằng CAKE, được sử dụng để đốt, góp phần giảm nguồn cung token và tăng giá trị dài hạn cho hệ sinh thái\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152744/ifo.png)  Play**Prediction**Prediction của PancakeSwap là một trò chơi dự đoán phi tập trung, đơn giản và thú vị, cho phép người dùng dự đoán giá BNBUSD, CAKEUSD hoặc ETHUSD sẽ tăng (UP) hay giảm (DOWN) trong các vòng kéo dài 5 phút (hoặc 10 phút trên zkSync). Người chơi đặt cược bằng BNB, CAKE hoặc ETH tùy thuộc vào thị trường, và nếu dự đoán đúng, họ chia sẻ quỹ thưởng của vòng.\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152822/prediction.png)  **Lottery**Lottery của PancakeSwap là trò chơi minh bạch, dễ tham gia, cho phép người dùng mua vé bằng CAKE (giá ~5 USD/vé, tối đa 100 vé/lần) để có cơ hội nhận thưởng lớn. Người chơi chọn 6 số, khớp càng nhiều số với kết quả ngẫu nhiên (dùng Chainlink VRF) càng nhận thưởng cao, từ giải nhỏ đến độc đắc. Tổng giải thưởng gồm CAKE từ vé bán và 10,000 CAKE bổ sung mỗi 2 ngày. Mua nhiều vé được chiết khấu, nhưng tăng nhẹ phí giao dịch. Một phần CAKE được đốt để giảm phát. Mỗi vòng kéo dài 12 giờ, vé không hoàn lại, kết quả kiểm tra thủ công. Lottery v2 tăng số khớp từ 4 lên 6, nâng cơ hội trúng giải nhỏ và tích lũy quỹ lớn hơn.\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152856/lottery.png)   \n ## Vậy PancakeSwap Caputure Value cho CAKE như thế nào?\n\nPancakeSwap đang tạo nên một cuộc cách mạng với mô hình Mint &amp; Burn kết hợp cùng veCAKE và hệ thống biểu quyết gauges, trao quyền cho người sở hữu CAKE để định hình tương lai của các liquidity pool. Bằng cách bỏ phiếu, veCAKE Holder có thể phân bổ CAKE Emission, ưu tiên các pool hoặc dự án yêu thích, mở ra cơ hội tối ưu hóa phần thưởng. Với veCAKE, bạn không chỉ là người tham gia mà còn là người dẫn dắt hệ sinh thái!\n\nveCAKE\n\n Holders có thể:\n\n- **Điều khiển Emission\n\n**: Trực tiếp quyết định cách phân bổ CAKE cho từng pool thanh khoản, dựa trên quyền biểu quyết tỷ lệ với số dư veCAKE. Quyền lực của bạn càng lớn, tác động càng sâu!\n\n\n- **Hợp tác với giao thức bên thứ ba\n\n**: Ủy quyền veCAKE cho các Liquid Wrappers hoặc thị trường Bribe để tự động hóa biểu quyết, nhận phần thưởng hấp dẫn hơn.\n\n\n- **Chinh phục hệ sinh thái PancakeSwap\n\n**: Power từ veCAKE (số lượng CAKE * thời gian lock) sẽ là thông số cho iCAKE (dùng cho IFO), bCAKE (dùng cho boosting yields farming).\n\n\nCơ chế Mint &amp; Burn – Tăng giá trị bền vững: Ngoài việc phân phối phần thưởng qua các sản phẩm, PancakeSwap đốt CAKE từ nhiều nguồn để giảm nguồn cung, đẩy giá trị lâu dài:\n\n- 0.001-0.23% phí giao dịch trên Exchange V3 (trừ Aptos).\n\n\n- 0.0575% phí giao dịch trên Exchange V2.\n\n\n- 0.004-0.02% phí từ StableSwap.\n\n\n- 20% lợi nhuận từ Perpetual Trading.\n\n\n- 100% phí hiệu suất CAKE từ IFO.\n\n\n- 100% CAKE dùng cho Profile Creation và NFT minting.\n\n\n- 100% CAKE từ người thắng Farm Auctions.\n\n\n- 2% doanh thu bán NFT trên NFT Market.\n\n\n- 20% CAKE từ \n\nviệc mua vé Lottery.\n\n\n- 3% mỗi \n\nround BNB/CAKE Prediction Markets\n\n dùng mua lại CAKE để burn.\n\n\n- 80% doanh thu từ bán tên miền .cake.\n\n\n![](https://statics.gemxresearch.com/images/2025/04/11/152944/tokenomic.png)  Đề xuất bỏ veTOKEN\n\nDù mô hình veCAKE ra mắt năm 2023 từng tạo dấu ấn với quyền biểu quyết mạnh mẽ, PancakeSwap nay đưa ra Đề xuất Tokenomics 3.0, quyết định gỡ bỏ hệ thống này để khắc phục những hạn chế cản bước hệ sinh thái.\n\nTrước hết, veCAKE tạo ra hệ thống quản trị phức tạp, yêu cầu khóa token dài hạn, khiến nhiều người dùng khó tiếp cận và làm giảm sự tham gia cộng đồng. Thứ hai, \n\ncơ chế gauges phân bổ phần thưởng thiếu hiệu quả\n\n, khi các pool thanh khoản nhỏ nhận tới 40% CAKE Emission nhưng chỉ đóng góp dưới 2% vào doanh thu, gây lãng phí tài nguyên.\n\nBên cạnh đó, việc khóa CAKE dài hạn làm mất tính linh hoạt, hạn chế quyền tự do sở hữu tài sản. Cuối cùng, sự thiếu đồng bộ giữa Emission và giá trị kinh tế từ các pool tạo ra mất cân bằng, ảnh hưởng đến lợi ích chung.\n\nVới Tokenomics 3.0, PancakeSwap mở ra một kỷ nguyên mới, tập trung vào bốn mục tiêu lớn lao:\n\n- Tăng quyền sở hữu thực sự: Xóa bỏ staking CAKE, veCAKE, gauges và chia sẻ doanh thu, trao trả tự do sử dụng token cho người dùng mà không cần khóa dài hạn.\n\n\n- Đơn giản hóa quản trị: Thay thế mô hình veCAKE rườm rà bằng hệ thống linh hoạt, chỉ cần stake CAKE trong thời gian biểu quyết, mở cửa cho mọi người tham gia dễ dàng.\n\n\n- Tăng trưởng bền vững: \n\nĐặt mục tiêu giảm phát 4%/năm\n\n, giảm 20% nguồn cung CAKE đến 2030. Lượng Emission CAKE hàng ngày giảm từ 40,000 xuống 22,500 qua ba giai đoạn, được đội ngũ quản lý dựa trên dữ liệu thị trường thời gian thực, ưu tiên pool thanh khoản lớn để tăng hiệu quả 30-40%. \n\nToàn bộ phí giao dịch chuyển sang đốt CAKE, nâng tỷ lệ đốt ở một số pool từ 10% lên 15\n\n%.\n\n\n- Hỗ trợ cộng đồng: Mở khóa toàn bộ CAKE đã stake và veCAKE mà không phạt, với thời hạn rút 6 tháng qua giao diện PancakeSwap. Người dùng veCAKE từ bên thứ ba (như CakePie, StakeDAO) sẽ chờ đối tác triển khai rút.\n\n\n \n ## Onchain Insights\n\n \n ### Các sản phẩm\n\nChúng ta đã nắm rõ cách CAKE tạo giá trị thông qua veTOKEN và cơ chế Mint &amp; Burn trong hệ sinh thái PancakeSwap. Xét về sản phẩm Lottery, doanh thu từ bán vé (Ticket Sale) trong 90 ngày từ 03/01 đến 14/04/2024 cho thấy xu hướng tăng trưởng không ổn định, với những giai đoạn tăng giảm rõ rệt. Cụ thể, Lottery ghi nhận các đợt tăng trưởng mạnh như 200% vào đầu tháng 1, 100% vào đầu tháng 2 và giữa tháng 3, nhưng cũng đối mặt với những đợt sụt giảm đáng kể từ 33% đến 50%, đặc biệt giảm mạnh vào cuối tháng 3 và đầu tháng 4. Dù có phục hồi nhẹ 50% vào ngày 14/4, mức tăng này không đủ để bù đắp cho sự sụt giảm trước đó, cho thấy Lottery chưa tạo được sức hút bền vững.\n\nĐối với sản phẩm Prediction, phí giao dịch trên BNB Chain (tính bằng USD) từ ngày 01/01/2024 đến 08/04/2024 cho thấy xu hướng tăng trưởng mạnh mẽ ban đầu, sau đó giảm dần nhưng vẫn duy trì ở mức cao hơn so với đầu kỳ. Cụ thể, phí giao dịch tăng đột biến từ 15K USD vào ngày 01/01 lên mức đỉnh 157.9K USD vào ngày 24/01, tương ứng với mức tăng trưởng ấn tượng 952.67%. Tuy nhiên, sau khi đạt đỉnh, phí bắt đầu giảm dần, dao động từ 149.4K USD (ngày 07/02) xuống 117K USD (ngày 07/03), rồi phục hồi nhẹ lên 123.6K USD (ngày 14/03), trước khi tiếp tục giảm còn 91.1K USD vào ngày 08/04. Từ mức đỉnh đến cuối kỳ, phí giảm 42.30%, tương đương 66.8K USD. Dù vậy, so với đầu kỳ, phí giao dịch vẫn tăng trưởng mạnh 507.33%, từ 15K USD lên 91.1K USD.\n\nTại Perp, từ năm 2023 đến nay, mức phí thu được đạt đỉnh vào cuối quý 1/2024 với tổng cộng $330,673, ghi nhận mức tăng trưởng ấn tượng 1059.6% so với tháng 4/2023. Tuy nhiên, từ quý 2/2024, nguồn phí này bắt đầu suy giảm và kéo dài đến thời điểm hiện tại. So với mức phí cao nhất mọi thời đại (ATH) vào ngày 08/03/2024, con số này đã giảm mạnh xuống còn $20,451, tương ứng với mức giảm 93.8%. Về đóng góp, phần lớn phí đến từ BSC và ARB, trong khi OPBNB và Base chỉ chiếm một phần rất nhỏ, gần như không đáng kể trong tổng thể.\n\n \n ### Token\n\nVề lượng CAKE, hơn 93% được khóa để nhận veCAKE, trong khi 6.7% còn lại được phân bổ vào các Pool khác nhau (CAKE Pool). Từ tháng 1/2024 đến nay, xu hướng Net Mint của CAKE chủ yếu âm, cho thấy nguồn cung đang giảm phát một cách tích cực. Điều này phản ánh các sản phẩm trong hệ sinh thái CAKE vẫn duy trì đủ nhu cầu để thúc đẩy lượng Burn hàng tuần.\n\nDù PancakeSwap sở hữu nhiều sản phẩm đa dạng ngoài AMM và tích hợp chúng vào cơ chế Mint &amp; Burn, phần lớn lượng Burn lại đến từ hoạt động trên AMM Dex, trong khi các sản phẩm khác chỉ đóng góp khoảng 11.1% vào quá trình Burn. Điều này cho thấy AMM vẫn là động lực chính trong việc duy trì cơ chế giảm phát của CAKE.\n\n \n ## Tổng kết\n\nMô hình của Pancake nổi bật với sự đa dạng vượt trội so với các sàn DEX khác, không chỉ dừng lại ở DEX mà còn tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn, tạo sự cân bằng với lượng Emission để thu hút thanh khoản. Điểm nhấn là cơ chế veTOKEN, về lý thuyết, giúp khóa nguồn cung, giảm áp lực bán tháo lên biểu đồ giá. Tuy nhiên, thực tế lại cho thấy veTOKEN gây ra không ít trở ngại trong việc điều phối Emission, dẫn đến hạn chế cho các Liquidity Pools có TVL thấp, làm dấy lên những thách thức trong vận hành.\n\nDù Pancake hướng đến xây dựng một hệ sinh thái linh hoạt, bền vững, ưu tiên lợi ích cộng đồng và hiệu quả dài hạn, nhưng các đề xuất gần đây lại vấp phải tranh cãi xoay quanh tính phi tập trung và niềm tin từ cộng đồng. Những cuộc tranh luận này phản ánh sự cạnh tranh khốc liệt và cả những \"trò chơi chính trị\" trong nội bộ hệ sinh thái.\n\nMột vấn đề đáng chú ý là sự xuất hiện của các Liquid Wrappers – một hiện tượng phổ biến trong các dự án áp dụng mô hình veTOKEN, nhằm chiếm quyền sở hữu lượng lớn veTOKEN. Tuy nhiên, Pancake bị nghi ngờ đã âm thầm tích lũy CAKE để nâng tỷ lệ sở hữu veTOKEN lên gần 50%, vượt mặt các Liquid Wrappers. Đỉnh điểm là đề xuất loại bỏ hoàn toàn veTOKEN, gây ra nhiều tranh cãi.\n\n [Twitter Post](https://twitter.com/defiwars_/status/1909955376147059114)Nếu đề xuất này được thông qua, các Liquid Wrappers phụ thuộc vào veTOKEN sẽ đối mặt với nguy cơ sụp đổ hoàn toàn, do bản chất tồn tại của chúng dựa vào lượng veTOKEN nắm giữ. Mặt khác, việc loại bỏ veTOKEN có thể mang lại lợi ích lớn hơn cho Pancake, củng cố mô hình Mint &amp; Burn và gia tăng giá trị cho CAKE. Tuy nhiên, động thái này không chỉ là một quyết định chiến lược mà còn là một bước đi đầy rủi ro, có thể định hình lại niềm tin và tương lai của hệ sinh thái Pancake.\n\n&nbsp;\n\n**Tất cả chỉ vì mục đích thông tin tham khảo, bài viết này hoàn toàn không phải là lời khuyên đầu tư\n\n     ** &nbsp;\n\nHy vọng với những thông tin trên sẽ giúp các bạn có nhiều insights thông qua \n\nCapWheel Series Pancake Swap\n\n. Những thông tin về dự án mới nhất sẽ luôn được cập nhật nhanh chóng trên website và các kênh chính thức của \n\nGFI Research\n\n. Các bạn quan tâm đừng quên tham gia vào nhóm cộng đồng của GFI để cùng thảo luận, trao đổi kiến thức và kinh nghiệm với các thành viên khác nhé.\n\n     &nbsp;\n\n&nbsp;\n\n\n\n\n    ~~~metadata \n\n    undefined: undefined\nundefined: undefined\nundefined: undefined\nExcerpt: Pancake nổi bật so với các sàn DEX khác nhờ hệ sinh thái đa dạng, tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn trong mô hình Mint & Burn của CAKE. Tuy nhiên, phần lớn lượng CAKE được Burn vẫn đến từ các hoạt động DEX, trong khi các sản phẩm khác chỉ đóng góp khoảng 11% vào tổng lượng Burn.\n\nĐề xuất loại bỏ veCAKE được đưa ra với mục tiêu kiểm soát nguồn cung hiệu quả hơn, nhưng lại vấp phải tranh cãi gay gắt về tính phi tập trung. Pancake bị nghi ngờ đã có những động thái không minh bạch nhằm giảm sức ép từ các Liquid Wrappers trước khi đề xuất được đưa vào biểu quyết, làm dấy lên nhiều lo ngại trong cộng đồng.\nundefined: undefined\nundefined: undefined\nMeta description: Pancake nổi bật so với các sàn DEX khác nhờ hệ sinh thái đa dạng, tích hợp nhiều sản phẩm nhằm thúc đẩy cơ chế Burn trong mô hình Mint & Burn.\n postUrl: capwheel-series-pancakeswap \n ~~~"

    topic_and_style = '''
🧠 Chủ đề chính thường gặp trên GFI Research
Phân tích dự án Web3 & DeFi
Ví dụ: LayerZero, EigenLayer, zkSync, Starknet,...
Tập trung vào công nghệ lõi, roadmap, và khả năng tăng trưởng.
Tokenomics & Định giá
Phân tích cơ cấu phân phối token, lịch unlock, vốn hóa, FDV.
So sánh với các dự án tương tự trong cùng phân khúc.
Góc nhìn đầu tư & Chiến lược danh mục
Đưa ra đề xuất phân bổ vốn theo từng nhóm dự án.
Phân tích lợi suất kỳ vọng, rủi ro thị trường, và xu hướng dòng tiền.
Tổng hợp dữ liệu thị trường & On-chain
Sử dụng dữ liệu thực tế từ Dune Analytics, TradingView, v.v.
Cập nhật về giá, khối lượng giao dịch, TVL, và các chỉ số hành vi người dùng.
Cập nhật sự kiện & Tác động vĩ mô
Tin tức từ Fed, SEC, thị trường tiền pháp định ảnh hưởng tới crypto.
Các sự kiện như unlock token, mainnet launch, hard fork,...
✍️ Phong cách viết đặc trưng
Mang tính phân tích – không chỉ đưa tin
Tác giả thường đi sâu vào bản chất vấn đề (What – Why – So what).
Luôn có phần đánh giá hoặc quan điểm riêng đi kèm.
Sử dụng biểu đồ và dữ liệu nhiều
Biểu đồ trực quan hóa xu hướng giá, lịch unlock, chỉ số on-chain...
Có thể xuất phát từ API hoặc tool do GFI Research tự xây dựng.
Cấu trúc rõ ràng, theo định dạng nghiên cứu
Thường chia thành các phần: Giới thiệu, Phân tích, Nhận định, Kết luận.
Có mục lục nội dung nếu bài dài.
Giọng văn chuyên nghiệp nhưng dễ tiếp cận
Không dùng quá nhiều thuật ngữ chuyên sâu trừ khi cần thiết.
Mục tiêu phục vụ cộng đồng nhà đầu tư cá nhân, không chỉ developer.
Có góc nhìn định hướng đầu tư
Mỗi bài đều gợi mở ý tưởng hoặc đánh giá rủi ro/lợi nhuận.
Dù không khuyến nghị tài chính trực tiếp, nhưng rất định hướng hành vi. 
    '''

    # print(check_article_structure(llm, text))

    # print(check_content(llm,text))

    # print(check_grammar_error(llm,text))

    # print(suggest_url(llm,text))

    print(check_text(llm,text))