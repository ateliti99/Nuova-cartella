import openai

openaikey = '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'

def generate_prompt(travel_info: dict, txt: str) -> dict:
    """Generate a prompt for the GPT-3 API based on the user's input.

    Args:
        travel_info (dict): A dictionary containing the user's input.

    Returns:
        str: A string returned by the GPT-3 API.
    """
    prompt = f"""I want you to act as a travel guide. I will write you my location,
    my preferences, arrival date, departure date, transportations systems I want to use, 
    how many people we are and our ages, budget, and timeslot available for activity. 
    The date format is aaaa-mm-dd. You will suggest a list of places to visit near my location. 
    Return the results as a JSON with the list of the places with duration (format %h:%min) of 
    the visit and tag of the place. My preferences you need to use to personalize results 
    are: "{txt}". These are important pieces of information that you need to 
    use to refine the results: {str(travel_info)}\n"""
    
    openai.api_key = openaikey
    
    # Call the GPT-3 API
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n"]
    )
    
    # Return the response
    return response.choices[0].text