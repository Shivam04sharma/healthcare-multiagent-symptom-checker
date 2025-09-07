# multiple - agents
import json
import re
import os
from typing import List, Dict, Any, Optional
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.agents import AgentExecutor
from langchain.tools import BaseTool
import requests
from dotenv import load_dotenv

load_dotenv()

class SymptomAnalyzerAgent:
    # Agent responsible for parsing and normalizing user input symptoms. Converts free-text input into structured, standardized symptom data.
    def __init__(self):
        self.common_symptom_mappings = {
            # Pain-related
            "hurt": "pain", "ache": "pain", "sore": "pain", "painful": "pain",
            "throbbing": "pain", "sharp pain": "pain", "dull pain": "pain",
            
            # Respiratory
            "can't breathe": "difficulty breathing", "hard to breathe": "difficulty breathing",
            "stuffy nose": "nasal congestion", "blocked nose": "nasal congestion",
            "runny nose": "nasal discharge", "sniffles": "runny nose",
            
            # Digestive
            "stomach ache": "abdominal pain", "belly pain": "abdominal pain",
            "upset stomach": "nausea", "feel sick": "nausea",
            "loose stools": "diarrhea", "watery stools": "diarrhea",
            
            # General
            "tired": "fatigue", "exhausted": "fatigue", "worn out": "fatigue",
            "hot": "fever", "burning up": "fever", "temperature": "fever",
            "dizzy": "dizziness", "lightheaded": "dizziness",
            "itchy": "itching", "scratchy": "itching"
        }
    
    def analyze_symptoms(self, user_input: str, age: Optional[int] = None, 
                        chronic_conditions: Optional[str] = None) -> Dict[str, Any]:
        
        cleaned_input = self._clean_input(user_input)

        symptoms = self._extract_symptoms(cleaned_input)
        
        normalized_symptoms = self._normalize_symptoms(symptoms)
   
        severity_indicators = self._extract_severity(cleaned_input)
      
        duration = self._extract_duration(cleaned_input)
        
        return {
            "original_input": user_input,
            "cleaned_input": cleaned_input,
            "extracted_symptoms": symptoms,
            "normalized_symptoms": normalized_symptoms,
            "severity_indicators": severity_indicators,
            "duration": duration,
            "age": age,
            "chronic_conditions": chronic_conditions,
            "analysis_confidence": self._calculate_confidence(symptoms)
        }
    
    def _clean_input(self, text: str) -> str:
        
        text = text.lower().strip()
        
        text = re.sub(r'\s+', ' ', text)
        
        filler_words = ['um', 'uh', 'like', 'you know', 'i mean']
        for word in filler_words:
            text = text.replace(word, '')
        
        return text.strip()
    
    def _extract_symptoms(self, text: str) -> List[str]:
        symptoms = []
        
        # Common symptom patterns
        symptom_patterns = [
            r'(headache|head\s*ache)',
            r'(fever|temperature|hot|burning\s*up)',
            r'(cough|coughing)',
            r'(nausea|nauseous|feel\s*sick|upset\s*stomach)',
            r'(vomit|vomiting|throw\s*up)',
            r'(diarrhea|loose\s*stools|watery\s*stools)',
            r'(fatigue|tired|exhausted|worn\s*out)',
            r'(dizziness|dizzy|lightheaded)',
            r'(chest\s*pain|chest\s*hurt)',
            r'(shortness\s*of\s*breath|can\'t\s*breathe|hard\s*to\s*breathe)',
            r'(sore\s*throat|throat\s*pain)',
            r'(runny\s*nose|nasal\s*discharge)',
            r'(stuffy\s*nose|nasal\s*congestion|blocked\s*nose)',
            r'(abdominal\s*pain|stomach\s*ache|belly\s*pain)',
            r'(muscle\s*aches|body\s*aches)',
            r'(rash|skin\s*rash)',
            r'(itching|itchy)',
            r'(swelling|swollen)',
            r'(blurred\s*vision|vision\s*problems)',
            r'(difficulty\s*concentrating|can\'t\s*focus)'
        ]
        
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    symptoms.append(match[0])
                else:
                    symptoms.append(match)
        
        pain_patterns = [
            r'(\w+)\s*(pain|ache|hurt|sore)',
            r'(pain|ache|hurt|sore)\s*in\s*(\w+)',
            r'my\s*(\w+)\s*(hurts|aches|is\s*sore)'
        ]
        
        for pattern in pain_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    body_part = match[0] if 'pain' not in match[0] else match[1]
                    symptoms.append(f"{body_part} pain")
        
        return list(set(symptoms))  
    
    def _normalize_symptoms(self, symptoms: List[str]) -> List[str]:
        
        normalized = []
        
        for symptom in symptoms:
          
            normalized_symptom = self.common_symptom_mappings.get(symptom.lower(), symptom)
            normalized.append(normalized_symptom)
        
        return list(set(normalized))
    
    def _extract_severity(self, text: str) -> Dict[str, Any]:
      
        severity_indicators = {
            "mild": ["mild", "slight", "little", "minor"],
            "moderate": ["moderate", "medium", "noticeable"],
            "severe": ["severe", "intense", "extreme", "unbearable", "terrible", "awful", "excruciating"],
            "emergency": ["emergency", "urgent", "can't", "unable", "worst", "never felt"]
        }
        
        detected_severity = "unknown"
        severity_score = 0
        
        for severity, keywords in severity_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    if severity == "emergency":
                        severity_score = 4
                        detected_severity = "emergency"
                    elif severity == "severe" and severity_score < 3:
                        severity_score = 3
                        detected_severity = "severe"
                    elif severity == "moderate" and severity_score < 2:
                        severity_score = 2
                        detected_severity = "moderate"
                    elif severity == "mild" and severity_score < 1:
                        severity_score = 1
                        detected_severity = "mild"
        
        return {
            "detected_severity": detected_severity,
            "severity_score": severity_score,
            "severity_keywords": [kw for kw in sum(severity_indicators.values(), []) if kw in text]
        }
    
    def _extract_duration(self, text: str) -> Dict[str, Any]:
        """Extract duration information from text."""
        duration_patterns = [
            r'(\d+)\s*(day|days|week|weeks|month|months|year|years)',
            r'(yesterday|today|this\s*morning|last\s*night)',
            r'(sudden|suddenly|gradual|gradually)',
            r'(chronic|ongoing|persistent|constant)'
        ]
        
        duration_info = {
            "duration_mentioned": False,
            "duration_text": [],
            "onset_type": "unknown"
        }
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, text)
            if matches:
                duration_info["duration_mentioned"] = True
                duration_info["duration_text"].extend([str(match) for match in matches])
        
        
        if any(word in text for word in ["sudden", "suddenly", "all of a sudden"]):
            duration_info["onset_type"] = "acute"
        elif any(word in text for word in ["gradual", "gradually", "over time", "chronic"]):
            duration_info["onset_type"] = "chronic"
        
        return duration_info
    
    def _calculate_confidence(self, symptoms: List[str]) -> float:
        """Calculate confidence score based on symptom extraction quality."""
        if not symptoms:
            return 0.0
        
        base_confidence = min(len(symptoms) * 0.2, 0.8)
        
        medical_terms = ["fever", "nausea", "diarrhea", "headache", "chest pain", "shortness of breath"]
        specific_symptoms = sum(1 for symptom in symptoms if any(term in symptom.lower() for term in medical_terms))
        
        confidence_boost = specific_symptoms * 0.1
        
        return min(base_confidence + confidence_boost, 1.0)


class ConditionMapperAgent:
    #Agent responsible for mapping symptoms to potential medical conditions. Uses rule-based knowledge base and optional LLM enhancement.

    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_available = bool(self.groq_api_key)
    
    def _load_knowledge_base(self, path: str) -> Dict[str, Any]:
        
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Knowledge base file {path} not found. Using empty knowledge base.")
            return {"conditions": [], "emergency_symptoms": []}
    
    def map_conditions(self, analyzed_symptoms: Dict[str, Any]) -> Dict[str, Any]:
        
        symptoms = analyzed_symptoms.get("normalized_symptoms", [])
        
        rule_based_matches = self._rule_based_matching(symptoms)
   
        llm_enhanced_matches = []
        if self.groq_available and symptoms:
            try:
                llm_enhanced_matches = self._llm_enhanced_matching(analyzed_symptoms)
            except Exception as e:
                print(f"LLM matching failed: {e}")
        
        combined_matches = self._combine_matches(rule_based_matches, llm_enhanced_matches)
        
        return {
            "rule_based_matches": rule_based_matches,
            "llm_enhanced_matches": llm_enhanced_matches,
            "combined_matches": combined_matches,
            "matching_confidence": self._calculate_matching_confidence(symptoms, combined_matches),
            "groq_api_used": bool(llm_enhanced_matches)
        }
    
    def _rule_based_matching(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """Match symptoms to conditions using rule-based approach."""
        condition_scores = []
        
        for condition in self.knowledge_base.get("conditions", []):
            condition_symptoms = [s.lower() for s in condition.get("symptoms", [])]
            user_symptoms = [s.lower() for s in symptoms]
            
            matches = sum(1 for symptom in user_symptoms 
                         if any(cs in symptom or symptom in cs for cs in condition_symptoms))
            
            if matches > 0:
                total_condition_symptoms = len(condition_symptoms)
                match_percentage = matches / max(total_condition_symptoms, len(user_symptoms))
                
                condition_scores.append({
                    "condition": condition["name"],
                    "match_score": matches,
                    "match_percentage": match_percentage,
                    "severity": condition.get("severity", "unknown"),
                    "matched_symptoms": [s for s in user_symptoms 
                                       if any(cs in s or s in cs for cs in condition_symptoms)],
                    "recommendations": condition.get("recommendations", []),
                    "medicines": condition.get("medicines", [])
                })
        
        # Sort by match score and percentage
        condition_scores.sort(key=lambda x: (x["match_score"], x["match_percentage"]), reverse=True)
        
        return condition_scores[:5]  
    
    def _llm_enhanced_matching(self, analyzed_symptoms: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Use Groq API to enhance condition matching."""
        if not self.groq_api_key:
            return []
        
        symptoms = analyzed_symptoms.get("normalized_symptoms", [])
        age = analyzed_symptoms.get("age")
        chronic_conditions = analyzed_symptoms.get("chronic_conditions")
        
       
        prompt = self._create_groq_prompt(symptoms, age, chronic_conditions)
        
        try:
            response = self._call_groq_api(prompt)
            return self._parse_groq_response(response)
        except Exception as e:
            print(f"Groq API call failed: {e}")
            return []
    
    def _create_groq_prompt(self, symptoms: List[str], age: Optional[int], 
                           chronic_conditions: Optional[str]) -> str:
        """Create prompt for Groq API."""
        prompt = f"""You are a medical AI assistant. Based on the following symptoms, provide the top 3 most likely medical conditions.

Symptoms: {', '.join(symptoms)}
"""
        
        if age:
            prompt += f"Patient age: {age}\n"
        
        if chronic_conditions:
            prompt += f"Chronic conditions: {chronic_conditions}\n"
        
        prompt += """
Please respond in JSON format with 
{
  "conditions": [
    {
      "name": "Condition Name",
      "confidence": 0.85,
      "reasoning": "Brief explanation",
      "severity": "mild/moderate/severe/emergency"
    }
  ]
}

"""
        
        return prompt
    
    def _call_groq_api(self, prompt: str) -> str:
        """Make API call to Groq."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": [
                {"role": "system", "content": "You are a helpful medical AI assistant. Provide information for educational purposes only."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _parse_groq_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse Groq API response."""
        try:
            
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                parsed = json.loads(json_str)
                return parsed.get("conditions", [])
        except Exception as e:
            print(f"Failed to parse Groq response: {e}")
        
        return []
    
    def _combine_matches(self, rule_based: List[Dict], llm_enhanced: List[Dict]) -> List[Dict[str, Any]]:
        
        combined = {}
        
        # Add rule-based matches
        for match in rule_based:
            condition_name = match["condition"]
            combined[condition_name] = {
                "condition": condition_name,
                "rule_based_score": match["match_score"],
                "rule_based_percentage": match["match_percentage"],
                "llm_confidence": 0.0,
                "combined_score": match["match_score"],
                "severity": match["severity"],
                "recommendations": match["recommendations"],
                "medicines": match["medicines"],
                "matched_symptoms": match.get("matched_symptoms", [])
            }
        
        # Add LLM matches
        for match in llm_enhanced:
            condition_name = match.get("name", "")
            if condition_name in combined:
                combined[condition_name]["llm_confidence"] = match.get("confidence", 0.0)
                combined[condition_name]["combined_score"] += match.get("confidence", 0.0) * 2
            else:
                combined[condition_name] = {
                    "condition": condition_name,
                    "rule_based_score": 0,
                    "rule_based_percentage": 0.0,
                    "llm_confidence": match.get("confidence", 0.0),
                    "combined_score": match.get("confidence", 0.0),
                    "severity": match.get("severity", "unknown"),
                    "recommendations": [],
                    "medicines": [],
                    "matched_symptoms": []
                }
        
        
        result = list(combined.values())
        result.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return result[:5]  
    
    def _calculate_matching_confidence(self, symptoms: List[str], matches: List[Dict]) -> float:
        """Calculate overall confidence in condition matching."""
        if not symptoms or not matches:
            return 0.0
        
       
        symptom_factor = min(len(symptoms) / 5.0, 1.0)  
        
        if matches:
            best_match_score = matches[0].get("combined_score", 0)
            match_factor = min(best_match_score / 3.0, 1.0)  
        else:
            match_factor = 0.0
        
        return (symptom_factor + match_factor) / 2.0


class AdvisorAgent:
    #Agent responsible for providing medical advice and detecting emergency situations. Analyzes symptoms and conditions to provide appropriate recommendations.
    
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.emergency_symptoms = self.knowledge_base.get("emergency_symptoms", [])
    
    def _load_knowledge_base(self, path: str) -> Dict[str, Any]:
       
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Knowledge base file {path} not found. Using empty knowledge base.")
            return {"conditions": [], "emergency_symptoms": []}
    
    def provide_advice(self, analyzed_symptoms: Dict[str, Any], 
                      condition_mappings: Dict[str, Any]) -> Dict[str, Any]:
        
        symptoms = analyzed_symptoms.get("normalized_symptoms", [])
        severity_info = analyzed_symptoms.get("severity_indicators", {})
        conditions = condition_mappings.get("combined_matches", [])
        
      
        emergency_alert = self._check_emergency_symptoms(symptoms, severity_info)
        
        
        recommendations = self._generate_recommendations(conditions, emergency_alert)
        
        medicine_suggestions = self._suggest_medicines(conditions)
        
        general_advice = self._generate_general_advice(symptoms, severity_info, emergency_alert)
        
        return {
            "emergency_alert": emergency_alert,
            "recommendations": recommendations,
            "medicine_suggestions": medicine_suggestions,
            "general_advice": general_advice,
            "disclaimer": self._get_disclaimer(),
            "when_to_seek_help": self._when_to_seek_help(symptoms, conditions, emergency_alert)
        }
    
    def _check_emergency_symptoms(self, symptoms: List[str], 
                                 severity_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check for emergency symptoms that require immediate attention."""
        emergency_detected = False
        emergency_symptoms_found = []
        emergency_level = "none"
        
        for symptom in symptoms:
            for emergency_symptom in self.emergency_symptoms:
                if emergency_symptom.lower() in symptom.lower() or symptom.lower() in emergency_symptom.lower():
                    emergency_detected = True
                    emergency_symptoms_found.append(emergency_symptom)
       
        if severity_info.get("detected_severity") == "emergency":
            emergency_detected = True
            emergency_level = "critical"
        elif emergency_symptoms_found:
            emergency_level = "high"
        
        emergency_patterns = [
            ("chest pain", "Possible heart attack - seek immediate medical attention"),
            ("difficulty breathing", "Respiratory emergency - call 108"),
            ("severe headache", "Possible stroke or serious condition"),
            ("abdominal pain", "Possible appendicitis or serious condition"),
            ("facial drooping", "Possible stroke - call 108 immediately"),
            ("speech difficulties", "Possible stroke - call 108 immediately")
        ]
        
        emergency_messages = []
        for symptom in symptoms:
            for pattern, message in emergency_patterns:
                if pattern in symptom.lower():
                    emergency_messages.append(message)
                    emergency_detected = True
                    emergency_level = "critical"
        
        return {
            "emergency_detected": emergency_detected,
            "emergency_level": emergency_level,
            "emergency_symptoms": emergency_symptoms_found,
            "emergency_messages": list(set(emergency_messages)),
            "call_108": emergency_level == "critical"
        }
    
    def _generate_recommendations(self, conditions: List[Dict], 
                                emergency_alert: Dict[str, Any]) -> Dict[str, Any]:
        """ they give  recommendations based on conditions and emergency status."""
        if emergency_alert["emergency_detected"]:
            return {
                "priority": "EMERGENCY",
                "immediate_actions": [
                    "CALL 108 IMMEDIATELY" if emergency_alert["call_108"] else "SEEK IMMEDIATE MEDICAL ATTENTION",
                    "Do not drive yourself to the hospital",
                    "Stay calm and follow emergency operator instructions",
                    "Have someone stay with you if possible"
                ],
                "avoid": [
                    "Do not take any medications unless prescribed",
                    "Do not eat or drink anything",
                    "Do not ignore symptoms"
                ]
            }
        
        recommendations = {
            "priority": "ROUTINE" if not conditions else "MODERATE",
            "immediate_actions": [],
            "self_care": [],
            "when_to_see_doctor": [],
            "avoid": []
        }
        
        for condition in conditions[:3]:  
            condition_recs = condition.get("recommendations", [])
            recommendations["self_care"].extend(condition_recs)
            
            severity = condition.get("severity", "mild")
            if severity in ["serious", "moderate"]:
                recommendations["when_to_see_doctor"].append(
                    f"Consider seeing a doctor for {condition['condition']}"
                )
                recommendations["priority"] = "MODERATE"
        
       
        recommendations["self_care"] = list(set(recommendations["self_care"]))
        recommendations["when_to_see_doctor"] = list(set(recommendations["when_to_see_doctor"]))
        
        # Add general advice
        if not recommendations["self_care"]:
            recommendations["self_care"] = [
                "Get adequate rest",
                "Stay hydrated",
                "Monitor your symptoms",
                "Maintain good hygiene"
            ]
        
        return recommendations
    
    def _suggest_medicines(self, conditions: List[Dict]) -> Dict[str, Any]:
        """Suggest over-the-counter medicines based on conditions."""
        medicine_suggestions = {
            "over_the_counter": [],
            "prescription_needed": [],
            "natural_remedies": []
        }
        
        # Collect medicines from conditions
        all_medicines = []
        for condition in conditions[:3]:
            medicines = condition.get("medicines", [])
            all_medicines.extend(medicines)
        
        # Categorize medicines
        otc_medicines = [
            "acetaminophen", "ibuprofen", "aspirin", "antihistamines", 
            "decongestants", "cough suppressants", "throat lozenges",
            "oral rehydration salts", "probiotics"
        ]
        
        natural_remedies = [
            "honey for cough", "ginger for nausea", "warm salt water gargle",
            "steam inhalation", "cold compress", "warm compress"
        ]
        
        for medicine in set(all_medicines):
            medicine_lower = medicine.lower()
            if any(otc in medicine_lower for otc in otc_medicines):
                medicine_suggestions["over_the_counter"].append(medicine)
            else:
                medicine_suggestions["prescription_needed"].append(medicine)
        
        
        medicine_suggestions["natural_remedies"] = natural_remedies[:3]
        
        return medicine_suggestions
    
    def _generate_general_advice(self, symptoms: List[str], severity_info: Dict[str, Any], 
                               emergency_alert: Dict[str, Any]) -> List[str]:
        """Generate general health advice."""
        if emergency_alert["emergency_detected"]:
            return [
                "This appears to be a medical emergency",
                "Seek immediate professional medical attention",
                "Do not delay in getting help"
            ]
        
        advice = [
            "Monitor your symptoms and note any changes",
            "Keep a symptom diary with dates and severity",
            "Stay hydrated and get adequate rest"
        ]
        
        # Add specific advice based on symptoms
        if any("fever" in s for s in symptoms):
            advice.append("Monitor your temperature regularly")
        
        if any("pain" in s for s in symptoms):
            advice.append("Apply appropriate heat or cold therapy")
        
        if any("nausea" in s or "vomiting" in s for s in symptoms):
            advice.append("Try small, frequent sips of clear fluids")
        
        if severity_info.get("detected_severity") in ["severe", "moderate"]:
            advice.append("Consider consulting with a healthcare provider")
        
        return advice
    
    def _when_to_seek_help(self, symptoms: List[str], conditions: List[Dict], 
                          emergency_alert: Dict[str, Any]) -> List[str]:
        
        if emergency_alert["emergency_detected"]:
            return ["SEEK IMMEDIATE EMERGENCY CARE"]
        
        seek_help_conditions = [
            "Symptoms worsen or don't improve after 3-5 days",
            "You develop a high fever (over 101.3°F/38.5°C)",
            "You experience severe pain",
            "You have difficulty breathing",
            "You become dehydrated",
            "You have concerns about your symptoms"
        ]
        
        # Add condition-specific guidance
        for condition in conditions[:2]:
            severity = condition.get("severity", "mild")
            if severity == "serious":
                seek_help_conditions.insert(0, f"You should see a doctor for suspected {condition['condition']}")
        
        return seek_help_conditions[:5]  
    
    def _get_disclaimer(self) -> str:
        
        return (
            "IMPORTANT DISCLAIMER: This symptom checker is for educational and informational "
            "purposes only. It is not intended to be a substitute for professional medical advice, "
            "diagnosis, or treatment. Always seek the advice of your physician or other qualified "
            "health provider with any questions you may have regarding a medical condition. "
            "Never disregard professional medical advice or delay in seeking it because of "
            "something you have read here. If you think you may have a medical emergency, "
            "call your doctor or 108/112 immediately."
        )


class MultiAgentOrchestrator:
    
    # Orchestrator class that manages the multi-agent workflow using LangChain concepts. Coordinates the interaction between AnalyzerAgent, ConditionMapperAgent, and AdvisorAgent.
    
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        self.analyzer_agent = SymptomAnalyzerAgent()
        self.mapper_agent = ConditionMapperAgent(knowledge_base_path)
        self.advisor_agent = AdvisorAgent(knowledge_base_path)
    
    def process_symptoms(self, user_input: str, age: Optional[int] = None, 
                        chronic_conditions: Optional[str] = None) -> Dict[str, Any]:
        
        try:
            
            print("Step 1: Analyzing symptoms...")
            analyzed_symptoms = self.analyzer_agent.analyze_symptoms(
                user_input, age, chronic_conditions
            )
            
            
            print("Step 2: Mapping conditions...")
            condition_mappings = self.mapper_agent.map_conditions(analyzed_symptoms)
            
            
            print("Step 3: Generating advice...")
            advice = self.advisor_agent.provide_advice(analyzed_symptoms, condition_mappings)
            
           
            complete_results = {
                "analyzed_symptoms": analyzed_symptoms,
                "condition_mappings": condition_mappings,
                "advice": advice,
                "processing_success": True,
                "error_message": None
            }
            
            return complete_results
            
        except Exception as e:
            print(f"Error in multi-agent processing: {e}")
            return {
                "analyzed_symptoms": {},
                "condition_mappings": {},
                "advice": {"error": str(e)},
                "processing_success": False,
                "error_message": str(e)
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        
        return {
            "analyzer_agent": {
                "status": "active",
                "capabilities": ["symptom parsing", "normalization", "severity detection"]
            },
            "mapper_agent": {
                "status": "active",
                "groq_available": self.mapper_agent.groq_available,
                "capabilities": ["rule-based matching", "LLM enhancement" if self.mapper_agent.groq_available else "rule-based only"]
            },
            "advisor_agent": {
                "status": "active",
                "capabilities": ["emergency detection", "recommendations", "medicine suggestions"]
            }
        }