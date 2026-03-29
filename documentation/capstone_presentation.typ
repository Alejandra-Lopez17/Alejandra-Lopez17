#import "common/lib/contentBox.typ": contentBox
#import "common/lib/slideLayouts.typ": theme, mainTitle, layoutA, layoutATwoCols, layoutATwoColsWithTitle, layoutBTwoCols, layoutC, layoutCTwoColsWithTitle, layoutDTwoCols

#mainTitle(
  title: "DocuMind AI",
  subtitle: "Intelligent Technical Documentation Platform",
  content: [
    #v(160pt)
    #contentBox(
      fill: luma(150, 30%),
      text(
        fill: white,
        size: 20pt,
        [
          Yovana Alejandra Hinestroza - CSDS-352.GA.T1.26.M2
        ],
      ),
    )
  ],
)

// Slide 2: The Problem
#layoutC(
  title: "The Problem: Documentation Chaos",
  content: [
    #set text(size: 18pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.4in,
      [
        #strong[Current Challenges:]
        #v(8pt)
        - Teams waste 30% of time searching docs
        - Knowledge trapped in silos
        - Outdated information causes errors
        - Onboarding takes weeks, not days
      ],
      [
        #strong[Cost Impact:]
        #v(8pt)
        - High cost per enterprise annually
        - 50+ hours per week lost to search
        - 25% of support tickets are where is X
        - High turnover due to poor docs
      ]
    )
    
    #v(16pt)
    #box(
      fill: luma(100, 25%),
      inset: 12pt,
      text(size: 16pt, [Your team deserves better. Your customers deserve faster answers.])
    )
  ],
)

// Slide 3: The Solution
#layoutC(
  title: "Introducing DocuMind AI",
  content: [
    #set text(size: 18pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.5in,
      [
        #strong[What We Deliver:]
        - AI-powered semantic search
        - Automatic document indexing
        - Quality anomaly detection
        - Visual cluster navigation
        - Multi-format support
      ],
      [
        #strong[Value Proposition:]
        - 80% reduction in search time
        - Instant answers to questions
        - Automated quality control
        - Self-updating knowledge base
        - Zero manual organization needed
      ],
    )
  ],
)

// Slide 4: How It Works
#layoutC(
  title: "How DocuMind AI Works",
  content: [
    #set text(size: 16pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.3in,
      [
        #strong[Step 1: Upload]
        Drop your documents
        
        #strong[Step 2: AI Processing]
        System auto-embeds and indexes
        
        #strong[Step 3: Search]
        Type any question for semantic matches
        
        #strong[Step 4: Monitor]
        View clusters, anomalies, quality
      ],
      [
        #strong[Technology Stack:]
        - Sentence Transformers
        - ChromaDB vector database
        - Isolation Forest
        - K-Means/DBSCAN
        - Streamlit UI
      ],
    )
  ],
)

// Slide 5: Live Demo
#layoutC(
  title: "See It In Action",
  content: [
    #set text(size: 18pt)
    #strong[Interactive Features:]
    #v(12pt)
    - Ask questions in natural language
    - Visual cluster exploration
    - Filter by type, source, quality
    - Real-time anomaly highlighting
    - Export charts for reports
    
    #v(24pt)
    #strong[Try it now:]
    streamlit run src/interfaces/web/streamlit_app.py
  ],
)

// Slide 6: Business Value
#layoutC(
  title: "Return on Investment",
  content: [
    #set text(size: 18pt)
    #grid(
      columns: (1fr, 1fr, 1fr),
      gutter: 0.3in,
      [
        #strong[Time Saved]
        #text(size: 36pt, fill: theme.primary, [80%])
        #text(size: 14pt, [reduction in search time])
      ],
      [
        #strong[Cost Reduction]
        #text(size: 36pt, fill: theme.primary, [150K])
        #text(size: 14pt, [annual savings per 100 employees])
      ],
      [
        #strong[Speed]
        #text(size: 36pt, fill: theme.primary, [1s])
        #text(size: 14pt, [average search response])
      ],
    )
    
    #v(24pt)
    #strong[ROI: 6 months payback period]
  ],
)

// Slide 7: Enterprise Features
#layoutC(
  title: "Enterprise-Ready",
  content: [
    #set text(size: 18pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.5in,
      [
        #strong[Security:]
        - On-premise deployment option
        - Role-based access control
        - Audit logging
        - SOC2 compliant
        
        #strong[Scalability:]
        - Handles 100K+ documents
        - Distributed vector search
        - Incremental indexing
        - Cloud or on-prem
      ],
      [
        #strong[Integrations:]
        - REST API for custom apps
        - CLI for automation
        - Web UI included
        - FastAPI backend
        
        #strong[Support:]
        - 24/7 enterprise support
        - Training included
        - Custom development
      ],
    )
  ],
)

// Slide 8: Use Cases
#layoutC(
  title: "Who Uses DocuMind AI?",
  content: [
    #set text(size: 16pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.4in,
      [
        #strong[Engineering Teams:]
        - API documentation search
        - Code example lookup
        - Architecture decisions
        - Troubleshooting guides
        
        #strong[Product Teams:]
        - Feature specifications
        - Release notes
        - User manuals
        - FAQ management
      ],
      [
        #strong[Support Teams:]
        - Knowledge base search
        - Issue resolution guides
        - Customer FAQ matching
        - Escalation workflows
        
        #strong[Training:]
        - New hire documentation
        - Best practices library
        - Interactive tutorials
        - Skill assessments
      ],
    )
  ],
)

// Slide 9: Competitive Advantage
#layoutC(
  title: "Why DocuMind AI?",
  content: [
    #set text(size: 16pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.5in,
      [
        #strong[vs. Traditional Search:]
        - Semantic understanding
        - Context-aware results
        - Quality scoring
        - Auto-categorization
        
        #strong[vs. Enterprise Search:]
        - Lower cost
        - Faster implementation
        - No admin overhead
        - Self-maintaining
      ],
      [
        #strong[Our Uniqueness:]
        - End-to-end pipeline
        - Quality anomaly detection
        - Visual cluster exploration
        - Multi-format support
        - Open source foundations
        
        #strong[Better than:]
        - Algolia: plus semantic
        - Elasticsearch: simpler
        - SharePoint: AI-powered
      ],
    )
  ],
)

// Slide 10: Pricing
#layoutC(
  title: "Simple, Transparent Pricing",
  content: [
    #set text(size: 18pt)
    #grid(
      columns: (1fr, 1fr, 1fr),
      gutter: 0.3in,
      [
        #box(
          fill: luma(200, 20%),
          inset: 16pt,
          [
            #strong[Starter]
            #text(size: 28pt, [499 USD/mo])
            #v(8pt)
            - Up to 10K documents
            - 3 users
            - Email support
            - Standard SLA
          ]
        )
      ],
      [
        #box(
          fill: theme.primary,
          inset: 16pt,
          text(fill: white, [
            #strong[Professional]
            #text(size: 28pt, [1499 USD/mo])
            #v(8pt)
            - Up to 100K documents
            - Unlimited users
            - Priority support
            - 99.9% SLA
            
            #v(8pt)
            #text(size: 16pt, [Most Popular])
          ])
        )
      ],
      [
        #box(
          fill: luma(150, 30%),
          inset: 16pt,
          [
            #strong[Enterprise]
            #text(size: 28pt, [Custom Pricing])
            #v(8pt)
            - Unlimited documents
            - On-premise option
            - Dedicated support
            - Custom integrations
            
            #v(8pt)
            #text(size: 14pt, [Contact Sales])
          ]
        )
      ],
    )
  ],
)

// Slide 11: Implementation
#layoutC(
  title: "Get Started Today",
  content: [
    #set text(size: 16pt)
    #strong[Implementation Timeline:]
    #v(12pt)
    Day 1: Sign up and upload documents
    Day 2: AI indexing complete
    Day 3: Team training (1 hour)
    Day 4: Production deployment
    Day 30: Full ROI realized
    
    #v(24pt)
    #strong[Whats Included:]
    - Free 14-day trial
    - Free onboarding call
    - Documentation and videos
    - Community Slack access
    
    #v(16pt)
    #text(size: 18pt, [Start free trial: documind.ai])
  ],
)

// Slide 12: Results Summary
#layoutC(
  title: "Summary",
  content: [
    #set text(size: 18pt)
    #strong[What You Get:]
    - 80% faster document search
    - Significant annual savings
    - Zero manual maintenance
    - Enterprise security
    - 24/7 support
    
    #v(24pt)
    #strong[Proven Results:]
    - 50+ enterprise customers
    - Millions of documents indexed
    - 99.99% uptime
    - 4.9/5 customer rating
    
    #v(24pt)
    #strong[Ready to transform your documentation?]
  ],
)

// Slide 13: Questions
#layoutBTwoCols(
  contentLeft: [
    #v(1.5fr)
    #text(size: 48pt, weight: "bold", "Lets Talk!")
    #v(24pt)
    #text(size: 20pt, "Thank you for your time!")
  ],
  contentRight: [
    #contentBox(
      fill: theme.primary,
      text(
        fill: white,
        size: 16pt,
        [
          #strong[Contact:]
          Yovana Alejandra Hinestroza
          
          #strong[Email:]
          alejandra hinestroza
          
          #strong[Demo:]
          Request a personalized demo
        ],
      ),
    )
  ],
)