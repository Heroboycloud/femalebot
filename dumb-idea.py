import random
from win10toast import ToastNotifier
toast=ToastNotifier() 
popularProductOrCompany = ["AirBnB", \
        "Uber", \
        "Apple", \
        "Netflix", \
        "Google", \
        "Facebook", \
        "Twitter", \
        "Spotify", \
        "SpaceX", \
        "Snapchat", \
        "Instagram", \
        "Juicero", \
        "Tinder", \
        "Tesla", \
        "Pinterest", \
        "SalesForce", \
        "WhatsApp", \
        "Slack", \
        "Lyft", \
        "YouTube", \
        "Siri"
]

industryOrPopularTech = ["Big Data", \
        "SaaS", \
        "IoT", \
        "FaaS", \
        "Kubernetes", \
        "Docker", \
        "Secrets Management", \
        "Crowdsourcing", \
        "On-Demand", \
        "Cloud", \
        "Machine Learning", \
        "AI", \
        "Data Mining", \
        "Distributed Teams", \
        "Observability", \
        "Distributed Systems", \
        "DevOps", \
        "Serverless", \
        "Progressive Web Apps", \
        "Crowd Sourcing", \
        "Cryptocurrency", \
        "BitCoin", \
        "3D Printing", \
        "Virtual Reality", \
        "Augmented Reality", \
        "the Gig Economy", \
        "Voice Interfaces"
]

idea=("It's like", popularProductOrCompany[random.randint(0, \
    len(popularProductOrCompany) - 1)], "for", \
    industryOrPopularTech[random.randint(0, len(industryOrPopularTech) - 1)])
idea=' '.join(idea)
toast.show_toast(title="New Dumb idea",msg=idea,duration=0.4)