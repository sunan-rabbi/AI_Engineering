sunanResumeInformation = {

  "personal_info": {
    "name": "Sunan Rabbi",
    "title": "Full-Stack Developer",
    "summary": "A passionate web developer, driven by a passion for crafting engaging user interfaces. Problem solver and coding enthusiast.",
    "email": "sunanrabbi1918@gmail.com",
    "phone": "+8801875899096",
    "location": "Rajshahi, Bangladesh",
    "links": {
      "portfolio": "https://sunanrabbi.me",
      "linkedin": "https://linkedin.com/in/sunanrabbi",
      "github": "https://github.com/sunan-rabbi"
    }
  },
  "education": [
    {
      "degree": "BSc in Computer Science and Engineering",
      "institution": "Rajshahi University of Engineering and Technology (RUET)",
      "location": "Rajshahi, Bangladesh",
      "duration": "12/2022 - Present"
    }
  ],
 "technical_skills": {
    "languages": ["JavaScript", "Python"],
    "frontend": ["React", "Next.js", "Redux"],
    "backend_and_api": ["Node.js", "GraphQL"],
    "databases_and_caching": ["MongoDB", "PostgreSQL", "Redis"],
    "cloud_and_devops": ["Docker", "AWS", "GitHub Actions", "Terraform"],
    "monitoring_and_observability": ["Grafana", "Prometheus", "Loki"],
    "data_analysis_and_mining": [
      "NumPy",
      "Pandas",
      "Matplotlib",
      "Seaborn",
      "Data Mining",
      "Predictive Modeling"
    ],
    "ai_and_machine_learning": [
      "Linear Regression",
      "Logistic Regression",
      "Perceptron",
      "Decision Trees",
      "RAG"
    ]
  },
  "work_experience": [
    {
      "role": "Junior Software Engineer",
      "company": "SasthoTech",
      "location": "Rajshahi, Bangladesh",
      "duration": "01/2025 - Present",
      "company_description": "Rajshahi-based health-tech company providing SaaS tools that automate hospital and diagnostic workflows for faster, smoother care.",
      "responsibilities_and_achievements": [
        "Built Digital Prescription Management System that replaces handwritten prescriptions with a fully digital solution, helping doctors generate clean, organized prescriptions.",
        "Worked on the Serial Management System by integrating the appointment creation form with the backend and developing the SMS purchase module.",
        "Developed a dynamic, multi-hospital report generation template that supports customizable layouts and automated data rendering.",
        "Developed a fully responsive marketing landing webpage using modern UI components and optimized layouts."
      ],
      "reference": {
        "name": "Shihab Sarar Islam Rafid",
        "phone": "+8801909793389"
      }
    },
    {
      "role": "Co-Founder & Software Engineer",
      "company": "Neural-bind",
      "location": "Rajshahi, Bangladesh",
      "duration": "06/2025 - Present",
      "company_description": "Affordable custom software, web & mobile apps, digital marketing, cybersecurity, and AI insights.",
      "responsibilities_and_achievements": [
        "Built and deployed the official website and landing page for Dream World Consultancy, enhancing their online presence.",
        "Developed a time and task management software for a Chinese company, improving workflow efficiency.",
        "Building a modern inventory management platform for retail and wholesale, featuring multi-role access, real-time tracking, and analytics.",
        "Developed an English-to-Chinese language learning app, enhancing language acquisition with interactive features."
      ],
      "reference": {
        "name": "Abdullah Al Noman",
        "email": "abdullahalnoman1120@gmail.com"
      }
    }
  ],
  "projects": [
    {
      "id": "prescription-management-system",
      "name": "Prescription Management System",
      "overview": "A specialized SaaS platform built to replace manual handwriting by generating clean, structured digital prescriptions tailored for clinics and hospitals.",
      "challenges_and_solutions": [
        {
          "challenge": "Dynamic Patient Data Collection",
          "details": "Different doctors require different patient intake fields (e.g., full contact data vs. only name and age).",
          "solution": "Built a custom settings dashboard allowing doctors to configure intake requirements, dynamically generating form inputs on the prescription page."
        },
        {
          "challenge": "Pixel-Perfect Print Formatting",
          "details": "Doctors use physical, pre-printed prescription pads with strict spatial constraints.",
          "solution": "Engineered strict print CSS layout calculations to map dynamic prescription data into pre-defined layouts without margin drift."
        },
        {
          "challenge": "Large-Scale Drug Catalog & Automated Advice",
          "details": "Managing a catalog of over 52,000 national medicines and speeding up consultation entries.",
          "solution": "Indexed the 52k medicine dataset for fast lookups and implemented an advisory preset system that auto-populates default guidelines (e.g., 'take before meals') upon medicine selection."
        }
      ]
    },
    {
      "id": "healthcare-service",
      "name": "Healthcare Service",
      "overview": "A comprehensive telemedicine platform enabling patients to book appointments and consult with physicians via live video calls.",
      "challenges_and_solutions": [
        {
          "challenge": "Real-Time Video Consultation Architecture",
          "details": "Establishing direct, low-latency in-browser communication as a major first production project.",
          "solution": "Implemented peer-to-peer WebRTC video streaming and real-time connection state management for stable consultations."
        },
        {
          "challenge": "Dynamic Chamber Slot & Queue Management",
          "details": "Preventing double-booking and managing wait times during live doctor consultations.",
          "solution": "Engineered an automated queue and slot management system tracking doctor availability, consultation durations, and patient transitions."
        }
      ]
    },
    {
      "id": "ticket-booking-site",
      "name": "Ticket Booking Site",
      "overview": "An online transit and bus ticketing platform designed to manage seat reservations, multi-stop route scheduling, and ticket sales.",
      "challenges_and_solutions": [
        {
          "challenge": "Multi-Segment Route Seat Allocation",
          "details": "Handling intermediate stops on routes (e.g., Rajshahi to Dhaka via Natore) without causing false vacancies or overbooking.",
          "solution": "Built a segment-aware booking engine: if a seat is reserved only from Rajshahi to Natore, the engine automatically marks that seat available from Natore to Dhaka for subsequent passengers."
        }
      ]
    },
    {
      "id": "inventory-management",
      "name": "Inventory Management",
      "overview": "A modern multi-tenant inventory platform for wholesale and retail operations featuring real-time tracking, role-based access, and analytics.",
      "challenges_and_solutions": [
        {
          "challenge": "Dynamic Tiered Subscription Pricing",
          "details": "Calculating fair billing for enterprise stores (multiple warehouses and staff) versus solo-owner shops (single branch, no employees).",
          "solution": "Designed a scalable tiered pricing engine that dynamically calculates billing based on active warehouse count and employee seats."
        },
        {
          "challenge": "Multi-Shop Data Isolation",
          "details": "Running multiple business tenants simultaneously from one centralized platform.",
          "solution": "Enforced strict role-based access control and tenant isolation so data never leaks between distinct shops."
        }
      ]
    },
    {
      "id": "ecommerce-drop-shipping",
      "name": "E-Commerce Site (Drop-Shipping Platform)",
      "overview": "A cross-border drop-shipping platform enabling consumers in Bangladesh to source products directly from Chinese suppliers.",
      "challenges_and_solutions": [
        {
          "challenge": "Massive Catalog Integration (1688 API)",
          "details": "Sourcing across 200M+ products and 1M+ suppliers made local database storage impossible.",
          "solution": "Created an on-demand synchronization layer querying the 1688 API in real time, mapping upstream vendor schemas directly into the platform's database structure."
        },
        {
          "challenge": "Multilingual Data Pipeline",
          "details": "Upstream vendor product titles, specs, and details were provided strictly in Mandarin.",
          "solution": "Built an automated content translation pipeline converting incoming Mandarin feeds into clean English or Bengali according to user preference."
        }
      ]
    }
  ],
  "organizations_and_leadership": [
    {
      "organization": "RUET Computing Society",
      "role": "Team Leader of Web Development Team",
      "duration": "08/2025 - Present"
    },
    {
      "organization": "RUET Career Forum",
      "role": "Executive Member",
      "duration": "06/2024 - 06/2025"
    },
    {
      "organization": "RUET Fitness Society",
      "role": "Membership Co-ordinator",
      "duration": "10/2025 - Present"
    }
  ],
  "certifications_and_awards": [
    {
      "title": "Winner at UIHP COHORT 4 (RUET)",
      "details": "Led team to 1st place, earning 55k BDT seed funding to develop our startup."
    },
    {
      "title": "AI Automation For Work & Business",
      "duration": "11/2025 - 12/2025",
      "details": "Built AI workflow automations and intelligent agents using n8n."
    },
    {
      "title": "Learnathon 3.0",
      "duration": "01/2025 - 05/2025",
      "details": "Participated in Learnathon 3.0 collaborating with teammates to complete learning tasks and solve problem-based challenges."
    },
    {
      "title": "Crash Course on Python",
      "duration": "08/2022 - 09/2022",
      "details": "Completed a foundational programming course covering Python syntax, functions, loops, data structures, and problem-solving."
    },
    {
      "title": "Inter School and College Programming Contest",
      "details": "Participated in the national round."
    }
  ]
  
}