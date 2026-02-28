def play_mad_libs():
    # Create a story
    story_template = "One day, a {animal} was going to {verb} for {food} in {location}."
    
    # Identify unique placeholders
    prompts = ["animal", "verb", "food", "location"]
    
    # Dictonary to store user responses
    user_responses = {}
    
    print("Welcome to Mad Libs! Please fill in the blanks:")
    
    for p in prompts:
        user_responses[p] = input("Enter a/an {}: ".format(p))
        
    # Use ** to unpack the dictonary into the format function
    final_story = story_template.format(**user_responses)
    
    print("\n" + final_story)
    
play_mad_libs()