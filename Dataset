import csv

def create_training_dataset():
    training_data = [
      import csv

        # Original data
        {"prompt": "A ___ is typically larger than a village but smaller than a city.", "answer": "town", "type": "cloze"},
        {"prompt": "The ___ is where the main government offices are located.", "answer": "capital", "type": "cloze"},
        {"prompt": "Many people enjoy living in the ___ because it is quieter than a city.", "answer": "suburb", "type": "cloze"},
        
        # New Cloze Tests
        {"prompt": "A ___ is a very small settlement with just a few houses.", "answer": "hamlet", "type": "cloze"},
        {"prompt": "The ___ area includes many factories and warehouses.", "answer": "industrial estate", "type": "cloze"},
        {"prompt": "Most people in this ___ work in agriculture.", "answer": "rural area", "type": "cloze"},
        {"prompt": "The ___ of London includes several boroughs.", "answer": "metropolitan area", "type": "cloze"},
        
        # Original Transformations
        {"prompt": "Express living in the outer part of Brest", "answer": "I live in the outskirts of Brest", "type": "transformation"},
        
        # New Transformations
        {"prompt": "Express that you live in an area with many houses built at the same time", "answer": "I live in a housing estate", "type": "transformation"},
        {"prompt": "Express that you live in a small community far from the city", "answer": "I live in a village", "type": "transformation"},
        {"prompt": "Express that you live in an area with many factories", "answer": "I live near an industrial estate", "type": "transformation"},
        
        # Original Translations
        {"prompt": "Translate 'city' to Russian", "answer": "город", "type": "translation"},
        {"prompt": "Translate 'suburb' to Russian", "answer": "пригород", "type": "translation"},
        
        # New Translations
        {"prompt": "Translate 'village' to Russian", "answer": "деревня", "type": "translation"},
        {"prompt": "Translate 'settlement' to Russian", "answer": "поселение", "type": "translation"},
        {"prompt": "Translate 'rural area' to Russian", "answer": "сельская местность", "type": "translation"},
        {"prompt": "Translate 'industrial estate' to Russian", "answer": "промышленная зона", "type": "translation"},
        {"prompt": "Translate 'housing estate' to Russian", "answer": "жилой массив", "type": "translation"},
        
        # Original Completions
        {"prompt": "Complete: A ___ often includes the city and its surrounding suburbs.", "answer": "metropolitan area", "type": "completion"},
        {"prompt": "Complete: Many people prefer living in a ___ due to its community facilities.", "answer": "housing estate", "type": "completion"},
        
        # New Completions
        {"prompt": "Complete: The new ___ was built to accommodate the growing population.", "answer": "settlement", "type": "completion"},
        {"prompt": "Complete: Living in a ___ means having easy access to nature.", "answer": "rural area", "type": "completion"},
        {"prompt": "Complete: The ___ has excellent transport links to the city center.", "answer": "residential area", "type": "completion"},
        
        # Original Abstract
        {
            "prompt": "Write about different types of human settlements without using direct vocabulary",
            "answer": "city, village, rural area",
            "type": "abstract",
            "context": "In many regions, various forms of human settlements exist. These can range from large centers of commerce and culture, which are bustling with activity, to smaller communities that offer a different pace of life."
        },
        
        # New Abstract
        {
            "prompt": "Describe the transition from rural to urban living without using direct vocabulary",
            "answer": "rural area, town, city, metropolitan area",
            "type": "abstract",
            "context": "As communities evolve, people often move from spaces dominated by nature and agriculture to more densely populated areas with modern amenities and infrastructure."
        },
        
        # Original Word Differences
        {"prompt": "Explain the difference between city and town", 
         "answer": "A city is typically larger and has more infrastructure compared to a town, which is smaller and often has a more close-knit community.",
         "type": "difference"},
        
        # New Word Differences
        {"prompt": "Explain the difference between village and hamlet",
         "answer": "A village is a small rural settlement with basic amenities, while a hamlet is an even smaller settlement with just a few houses and minimal facilities.",
         "type": "difference"},
        {"prompt": "Explain the difference between residential area and housing estate",
         "answer": "A residential area is any area where people live, while a housing estate is a planned development of houses built at the same time.",
         "type": "difference"},
        
        # Original Multiple Choice
        {"prompt": "The ___ (city/town) is the largest settlement in the region.", "answer": "city", "type": "multiple_choice"},
        {"prompt": "Many families choose to live in the ___ (suburb/country) for a quieter lifestyle.", "answer": "suburb", "type": "multiple_choice"},
        
        # New Multiple Choice
        {"prompt": "They built their house in a ___ (rural area/industrial estate) to enjoy the peaceful countryside.", "answer": "rural area", "type": "multiple_choice"},
        {"prompt": "The ___ (hamlet/metropolitan area) includes several million people.", "answer": "metropolitan area", "type": "multiple_choice"},
        {"prompt": "The new ___ (housing estate/industrial estate) will provide homes for 500 families.", "answer": "housing estate", "type": "multiple_choice"},
        
        # New Context-Based Questions
        {"prompt": "Describe the surroundings of your city", 
         "answer": "The surroundings of my city include suburbs, industrial estates, and rural areas with farms.",
         "type": "context",
         "context": "Using vocabulary related to city surroundings"},
        
        {"prompt": "How has your settlement changed over the years?",
         "answer": "Our village has grown into a town, with new housing estates and improved infrastructure.",
         "type": "context",
         "context": "Using vocabulary related to development and growth"}
  
        # New Exercise Type: Word Formation
        {"prompt": "Form an adjective from 'industry' to describe an area", "answer": "industrial", "type": "word_formation"},
        {"prompt": "Form an adjective from 'residence' to describe an area", "answer": "residential", "type": "word_formation"},
        {"prompt": "Form a noun from 'settle' to describe a place where people live", "answer": "settlement", "type": "word_formation"},
        {"prompt": "Form an adjective from 'metropolis' to describe a large city area", "answer": "metropolitan", "type": "word_formation"},
        
        # New Exercise Type: Collocations
        {"prompt": "What verb collocates with 'in a village'? (live/exist/stay)", "answer": "live in a village", "type": "collocation"},
        {"prompt": "What verb collocates with 'a settlement'? (establish/make/do)", "answer": "establish a settlement", "type": "collocation"},
        {"prompt": "What adjective collocates with 'metropolitan area'? (busy/crowded/dense)", "answer": "dense metropolitan area", "type": "collocation"},
        
        # New Exercise Type: Error Correction
        {"prompt": "Correct the error: 'I live on suburb'", "answer": "I live in a suburb", "type": "error_correction"},
        {"prompt": "Correct the error: 'The town is more bigger than village'", "answer": "The town is bigger than a village", "type": "error_correction"},
        {"prompt": "Correct the error: 'There is many industrial estates'", "answer": "There are many industrial estates", "type": "error_correction"},
        
        # New Exercise Type: Sentence Building
        {"prompt": "Build a sentence using 'suburb' and 'quiet'", "answer": "The suburb is a quiet place to live", "type": "sentence_building"},
        {"prompt": "Build a sentence using 'village' and 'traditional'", "answer": "The village maintains its traditional way of life", "type": "sentence_building"},
        {"prompt": "Build a sentence using 'city' and 'crowded'", "answer": "The city becomes crowded during rush hour", "type": "sentence_building"},
        
        # New Exercise Type: Word Association
        {"prompt": "Name three words associated with 'rural area'", "answer": "farms, nature, countryside", "type": "word_association"},
        {"prompt": "Name three words associated with 'industrial estate'", "answer": "factories, warehouses, manufacturing", "type": "word_association"},
        {"prompt": "Name three words associated with 'city center'", "answer": "shops, offices, restaurants", "type": "word_association"},
        
        # New Exercise Type: Definition Matching
        {"prompt": "Match the definition: 'An area where goods are manufactured'", "answer": "industrial estate", "type": "definition_matching"},
        {"prompt": "Match the definition: 'The parts of a city far from the center'", "answer": "outskirts", "type": "definition_matching"},
        {"prompt": "Match the definition: 'A planned group of houses built together'", "answer": "housing estate", "type": "definition_matching"},
        
        # New Exercise Type: Context Situations
        {
            "prompt": "What type of area would you recommend for someone who wants peace and quiet?",
            "answer": "I would recommend a rural area or village because they offer a peaceful environment away from city noise",
            "type": "situation",
            "context": "Giving advice about living locations"
        },
        {
            "prompt": "Where would you suggest a company build their new factory?",
            "answer": "They should build it in an industrial estate because it's designed for manufacturing and has good infrastructure",
            "type": "situation",
            "context": "Business location advice"
        },
        
        # New Exercise Type: Word Classification
        {
            "prompt": "Classify by size (largest to smallest): city, hamlet, town, village",
            "answer": "city, town, village, hamlet",
            "type": "classification",
            "context": "Settlement size ordering"
        },
        {
            "prompt": "Classify by population density: rural area, suburb, city center, industrial estate",
            "answer": "city center, suburb, industrial estate, rural area",
            "type": "classification",
            "context": "Population density ordering"
        },
        
        # New Exercise Type: Preposition Practice
        {"prompt": "Complete with preposition: He lives ___ the outskirts of the city.", "answer": "on", "type": "preposition"},
        {"prompt": "Complete with preposition: They moved ___ a new housing estate.", "answer": "to", "type": "preposition"},
        {"prompt": "Complete with preposition: The factory is located ___ an industrial estate.", "answer": "in", "type": "preposition"},
        
        # New Exercise Type: Vocabulary in Context
        {
            "prompt": "Read the text and fill the gaps: 'Many people are moving from the ___ to the ___ areas because they want to find better jobs.'",
            "answer": "rural, urban",
            "type": "context_gaps",
            "context": "Migration patterns"
        },
        {
            "prompt": "Read the text and fill the gaps: 'The ___ includes not only the city center but also the surrounding ___ .'",
            "answer": "metropolitan area, suburbs",
            "type": "context_gaps",
            "context": "City structure"
        }
    ]
    
    # Write to CSV file
    with open('extended_language_training_dataset.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['prompt', 'answer', 'type', 'context'])
        writer.writeheader()
        for item in training_data:
            writer.writerow(item)

if __name__ == "__main__":
    create_training_dataset()
