from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

class ActionStoreSymptoms(Action):
    def name(self) -> Text:
        return "action_store_symptoms"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = tracker.get_latest_entity_values("symptom")
        current_symptoms = tracker.get_slot("symptoms") or []
        emergency_symptoms = ["high fever", "severe pain", "difficulty breathing", "severe bleeding", "chest pain"]
        emergency_detected = any(symptom in emergency_symptoms for symptom in symptoms)

        for symptom in symptoms:
            if symptom not in current_symptoms:
                current_symptoms.append(symptom)

        # Check for partial or vague symptoms (e.g., single symptom)
        if len(current_symptoms) <= 1 and not emergency_detected:
            dispatcher.utter_message(text="Got it, but I might need more details to help you better.")
            return [SlotSet("symptoms", current_symptoms), FollowupAction("utter_ask_symptoms")]

        dispatcher.utter_message(text="Got it. I've noted your symptoms. What would you like to know? For example, you can ask what this might be or what you can take.")
        return [SlotSet("symptoms", current_symptoms), SlotSet("emergency_detected", emergency_detected)]

class ActionDiagnoseAilment(Action):
    def name(self) -> Text:
        return "action_diagnose_ailment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = tracker.get_slot("symptoms") or []
        if not symptoms:
            dispatcher.utter_message(text="I don't have any symptoms to analyze. Please tell me how you're feeling.")
            return []

        # Symptom-to-ailment mapping for 30 student-common ailments
        ailment_map = {
            ("fever", "cough", "sore throat"): "Common Cold",
            ("fever", "chills", "body ache", "fatigue"): "Influenza (Flu)",
            ("stomach pain", "nausea", "diarrhea"): "Gastroenteritis",
            ("headache", "fatigue", "neck stiffness"): "Tension Headache",
            ("itchy eyes", "runny nose", "sneezing"): "Allergic Rhinitis",
            ("red eyes", "itchy eyes", "eye discharge"): "Conjunctivitis (Pink Eye)",
            ("anxiety", "insomnia", "fatigue"): "Stress or Anxiety",
            ("fever", "swollen glands", "sore throat", "fatigue"): "Mononucleosis",
            ("cut", "bleeding"): "Minor Cut or Abrasion",
            ("rash", "itchiness"): "Contact Dermatitis",
            ("dizziness", "headache", "fatigue"): "Dehydration",
            ("sore throat", "fever", "white patches"): "Strep Throat",
            ("stuffy nose", "sinus pressure", "headache"): "Sinusitis",
            ("pimples", "oily skin"): "Acne",
            ("insomnia", "restlessness"): "Insomnia",
            ("ankle pain", "swelling"): "Sprain",
            ("ear pain", "hearing loss"): "Ear Infection",
            ("nausea", "vomiting", "abdominal pain"): "Food Poisoning",
            ("abdominal cramps", "bloating"): "Menstrual Cramps",
            ("wheezing", "shortness of breath"): "Mild Asthma",
            ("mouth sores", "painful swallowing"): "Canker Sores",
            ("back pain", "stiffness"): "Back Strain",
            ("burning urination", "frequent urination"): "Urinary Tract Infection",
            ("dry skin", "itchiness"): "Eczema",
            ("cough", "chest congestion"): "Bronchitis",
            ("joint pain", "stiffness"): "Overuse Injury",
            ("fatigue", "poor concentration"): "Sleep Deprivation",
            ("sneezing", "itchy throat"): "Seasonal Allergies",
            ("fever", "rash", "fatigue"): "Viral Exanthem",
            ("sore muscles", "fatigue"): "Post-Exercise Soreness",
        }

        possible_ailment = "Unknown condition"
        for symptom_set, ailment in ailment_map.items():
            if all(symptom in symptoms for symptom in symptom_set):
                possible_ailment = ailment
                break

        dispatcher.utter_message(text=f"Based on your symptoms ({', '.join(symptoms)}), you might have {possible_ailment}. Please consult a doctor for a proper diagnosis.")
        return []

class ActionRecommendDrug(Action):
    def name(self) -> Text:
        return "action_recommend_drug"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptoms = tracker.get_slot("symptoms") or []
        if not symptoms:
            dispatcher.utter_message(text="I don't have any symptoms to analyze. Please tell me how you're feeling.")
            return []

        # Same ailment mapping as above
        ailment_map = {
            ("fever", "cough", "sore throat"): "Common Cold",
            ("fever", "chills", "body ache", "fatigue"): "Influenza (Flu)",
            ("stomach pain", "nausea", "diarrhea"): "Gastroenteritis",
            ("headache", "fatigue", "neck stiffness"): "Tension Headache",
            ("itchy eyes", "runny nose", "sneezing"): "Allergic Rhinitis",
            ("red eyes", "itchy eyes", "eye discharge"): "Conjunctivitis (Pink Eye)",
            ("anxiety", "insomnia", "fatigue"): "Stress or Anxiety",
            ("fever", "swollen glands", "sore throat", "fatigue"): "Mononucleosis",
            ("cut", "bleeding"): "Minor Cut or Abrasion",
            ("rash", "itchiness"): "Contact Dermatitis",
            ("dizziness", "headache", "fatigue"): "Dehydration",
            ("sore throat", "fever", "white patches"): "Strep Throat",
            ("stuffy nose", "sinus pressure", "headache"): "Sinusitis",
            ("pimples", "oily skin"): "Acne",
            ("insomnia", "restlessness"): "Insomnia",
            ("ankle pain", "swelling"): "Sprain",
            ("ear pain", "hearing loss"): "Ear Infection",
            ("nausea", "vomiting", "abdominal pain"): "Food Poisoning",
            ("abdominal cramps", "bloating"): "Menstrual Cramps",
            ("wheezing", "shortness of breath"): "Mild Asthma",
            ("mouth sores", "painful swallowing"): "Canker Sores",
            ("back pain", "stiffness"): "Back Strain",
            ("burning urination", "frequent urination"): "Urinary Tract Infection",
            ("dry skin", "itchiness"): "Eczema",
            ("cough", "chest congestion"): "Bronchitis",
            ("joint pain", "stiffness"): "Overuse Injury",
            ("fatigue", "poor concentration"): "Sleep Deprivation",
            ("sneezing", "itchy throat"): "Seasonal Allergies",
            ("fever", "rash", "fatigue"): "Viral Exanthem",
            ("sore muscles", "fatigue"): "Post-Exercise Soreness",
        }

        # Recommendations for each ailment (OTC or self-care)
        drug_map = {
            "Common Cold": "Try over-the-counter antihistamines (e.g., loratadine) or decongestants (e.g., pseudoephedrine). Rest and drink plenty of fluids.",
            "Influenza (Flu)": "Use over-the-counter flu relief like DayQuil or NyQuil. Rest and hydrate, and see a doctor for possible antivirals if severe.",
            "Gastroenteritis": "Stay hydrated with oral rehydration solutions like Pedialyte. Avoid solid food temporarily and consult a doctor if persistent.",
            "Tension Headache": "Take ibuprofen or paracetamol. Rest in a quiet, dark room and try relaxation techniques.",
            "Allergic Rhinitis": "Use antihistamines like cetirizine or loratadine. Avoid allergens and consult a doctor if symptoms persist.",
            "Conjunctivitis (Pink Eye)": "Clean eyes with a warm, damp cloth. Avoid touching them and see a doctor, as some types need antibiotic drops.",
            "Stress or Anxiety": "Practice deep breathing or meditation. Consider talking to a counselor or doctor for ongoing issues.",
            "Mononucleosis": "Rest and hydrate. Avoid strenuous activity and consult a doctor, as this can be serious.",
            "Minor Cut or Abrasion": "Clean the wound with soap and water, apply an antiseptic like hydrogen peroxide, and cover with a bandage. See a doctor if deep or infected.",
            "Contact Dermatitis": "Apply hydrocortisone cream for itching. Avoid irritants and see a doctor if the rash worsens.",
            "Dehydration": "Drink water or an electrolyte drink. Eat a small snack and seek medical help if dizziness persists.",
            "Strep Throat": "Gargle with warm salt water for relief. See a doctor promptly, as antibiotics may be needed.",
            "Sinusitis": "Use a saline nasal spray or decongestant. A warm compress on the face may help. See a doctor if symptoms last.",
            "Acne": "Use over-the-counter benzoyl peroxide or salicylic acid products. Keep skin clean and consult a dermatologist if severe.",
            "Insomnia": "Try a consistent sleep schedule and avoid screens before bed. Consult a doctor if sleep issues persist.",
            "Sprain": "Rest, ice, compress, and elevate (RICE method). Use ibuprofen for pain and see a doctor if swelling persists.",
            "Ear Infection": "Apply a warm compress to the ear. See a doctor, as antibiotics may be needed for bacterial infections.",
            "Food Poisoning": "Stay hydrated with small sips of water or electrolyte drinks. Avoid food for a few hours and see a doctor if severe.",
            "Menstrual Cramps": "Take ibuprofen or naproxen. Use a heating pad on the lower abdomen and rest.",
            "Mild Asthma": "Use an over-the-counter inhaler if prescribed. Avoid triggers and consult a doctor for asthma management.",
            "Canker Sores": "Use over-the-counter oral gels like benzocaine. Avoid spicy foods and see a doctor if sores persist.",
            "Back Strain": "Rest and apply a heating pad. Take ibuprofen for pain and avoid heavy lifting. See a doctor if pain continues.",
            "Urinary Tract Infection": "Drink plenty of water and avoid irritants like caffeine. See a doctor promptly, as antibiotics are often needed.",
            "Eczema": "Use moisturizers or hydrocortisone cream for itching. Avoid irritants and consult a doctor for severe cases.",
            "Bronchitis": "Use a cough suppressant like dextromethorphan at night. Stay hydrated and see a doctor if symptoms worsen.",
            "Overuse Injury": "Rest the affected area and apply ice. Take ibuprofen for pain and avoid repetitive strain.",
            "Sleep Deprivation": "Establish a regular sleep schedule and limit caffeine. Consult a doctor if fatigue persists.",
            "Seasonal Allergies": "Take antihistamines like loratadine. Stay indoors during high pollen times and see a doctor if needed.",
            "Viral Exanthem": "Rest and hydrate. See a doctor to confirm the cause, as some rashes need medical attention.",
            "Post-Exercise Soreness": "Rest and apply ice or heat to sore muscles. Take ibuprofen if needed and stretch gently.",
            "Unknown condition": "I can't suggest a specific remedy without a clear diagnosis. Please consult a doctor for appropriate treatment."
        }

        possible_ailment = "Unknown condition"
        for symptom_set, ailment in ailment_map.items():
            if all(symptom in symptoms for symptom in symptom_set):
                possible_ailment = ailment
                break

        recommendation = drug_map.get(possible_ailment, drug_map["Unknown condition"])
        dispatcher.utter_message(text=f"For your symptoms ({', '.join(symptoms)}), {recommendation}")
        return []