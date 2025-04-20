import json
import os
from typing import List, Dict, Optional

class TeluguStopWords:
    """A class to manage Telugu stopwords for NLP preprocessing."""
    
    def __init__(self):
        """Initialize with comprehensive Telugu stopwords in Telugu script and English transliteration."""
        self.stopwords: Dict[str, List[str]] = {
            "telugu": [
                # Conjunctions
                "మరియు", "లేదా", "కానీ", "అయితే", "ఎందుకంటే", "కాబట్టి", "అందువల్ల", "మాత్రం",
                "అయినప్పటికీ", "కాకపోతే", "ఇంకా", "లేక", "లేకపోతే", "తప్ప", "కాని", "అంటే",
                "అందుకే", "గనుక", "అలాగే", "ఇలానే",
                # Pronouns
                "నేను", "మీరు", "నీవు", "అతను", "ఆమె", "ఇది", "అది", "వారు", "మేము", "వాళ్ళు",
                "ఈ", "ఆ", "ఎవరు", "ఏది", "ఎవరైనా", "ఏదైనా", "ఎవరూ", "ఏమీ", "ఎవరో", "ఏదో",
                "తాను", "తమ", "తన", "మన", "మనకి", "మనలో", "మనవాళ్ళు", "మీ", "మీతో", "మీద",
                "మీకు", "నాకు", "నన్ను", "నన్నే", "మా", "తనకి", "తనను", "తనతో", "తనపై",
                "దాని", "దానిలో", "దానివల్ల", "ఎవరికి", "ఎవరితో", "ఎవరినైనా", "ఇతడు", "అవి",
                "ఇవి", "వీటిని", "ఏవి", "ఏవైనా", "ఇంకెవరూ", "ఇంకా ఎవరు", "ఇంకా ఏమి",
                "ఎంతైనా", "ఎవడైనా", "మా వారికి", "వాళ్లపై", "దీనిపై", "ఆవిడ", "ఆయన",
                # Postpositions
                "లో", "పై", "కు", "నుండి", "వద్ద", "తో", "గురించి", "మధ్య", "ద్వారా", "కింద",
                "పక్కన", "వెంట", "కోసం", "లోపల", "వెలుపల", "వైపు", "దగ్గర", "మీద", "క్రింద",
                "పైన", "వరకు", "వలన", "కంటే",
                # Auxiliary Verbs
                "ఉంది", "ఉన్నాయి", "ఉందు", "ఉన్నాను", "ఉన్నాము", "ఉన్నారు", "ఉంటుంది",
                "ఉంటాయి", "ఉంటే", "ఉండి", "ఉన్నా", "ఉండాలి", "ఉండదు", "ఉండగా",
                "ఉండేవాడు", "ఉండేవారు", "ఉంటున్న", "అవుతుంది", "అవుతాను", "అవుతారు",
                "అయింది",
                # Adverbs
                "ఇప్పుడు", "అప్పుడు", "ఎప్పుడు", "ఎప్పుడైనా", "ఎక్కడ", "ఇక్కడ", "అక్కడ",
                "ఎలా", "చాలా", "కొంత", "పూర్తిగా", "దాదాపు", "త్వరలో", "వెంటనే", "మళ్ళీ",
                "ఎప్పటికీ", "ఎప్పటినుండి", "ఎంత", "ఎంతో", "ఎక్కువగా", "ఇంతవరకు",
                "ఇప్పటికే", "ఇప్పటివరకు", "అప్పటివరకు", "తరువాత", "ఆ తరువాత",
                "ఎప్పుడయినా", "ఎప్పటికైనా", "ఇప్పటికీ", "ఇప్పటికైనా", "అప్పటికప్పుడు",
                "ఇప్పటికప్పుడు", "కాసేపు", "ఇంతలో", "అంతలో", "పెద్దగా", "చిన్నగా",
                "మరీ అంతగా", "ముఖ్యంగా", "సాధారణంగా", "అప్పుడే", "ఇంతకు ముందే",
                "చాలా రోజుల తరువాత", "కొన్ని రోజుల తరువాత", "కొన్ని గంటల తరువాత",
                "కొన్ని నిమిషాల తరువాత",
                # Particles
                "కూడా", "మాత్రమే", "అసలు", "ఏమో", "అని", "అంటే", "గానీ", "వంటి", "లాంటి",
                "తప్ప", "ఒక్కసారి", "కనుక", "గనుక",
                # Interjections
                "అరె", "ఓహో", "అయ్యో", "హాయ్", "ఓ", "హే", "అబ్బా", "ఛీ", "అవును", "కాదు",
                "సరే", "అవునా", "అవుతుందా", "చాలు",
                # Quantifiers
                "అన్ని", "కొన్ని", "ప్రతి", "ఏ", "చాలా", "కొంచెం", "ఎక్కువ", "తక్కువ",
                "అనేక", "ఒకటి", "రెండు", "మూడు", "నాలుగు", "అందరూ", "అంత", "అంతే",
                "ఇంత", "ఇంతే",
                # Verbs (Common, Modal, Auxiliary)
                "వచ్చే", "వెళ్లే", "వెళ్లింది", "వచ్చింది", "తినే", "తిన్న", "తిన్నాను",
                "తినటం", "వద్దు", "వచ్చారు", "తిరిగి", "కూడదనుకుంటే", "వద్దనుకుంటే",
                "తినలేదు", "తిన్నా", "తినలేను", "వచ్చాను", "వెళ్లాను", "వెళ్ళలేదు",
                "వెళ్తాను", "వెళ్తాడు", "వెళ్తారు", "వస్తాను", "వస్తాడు", "వస్తారు",
                "తీసుకురా", "పంపించు", "తీసుకో", "ఇవ్వు", "తీసుకొమ్ము", "ఇవ్వండి",
                "వద్దురా", "వద్దండి", "చేసి", "చేసే", "చేసిన", "చేస్తున్న", "వెళ్తున్న",
                "వస్తున్న", "తీరా", "తలపెట్టే", "తలచే", "చూస్తే", "వినిపిస్తుంది", "వింటే",
                "చూడాలి", "తెలియదు", "తెలుస్తుంది", "ఉంచు", "వదిలివేయి", "పట్టించుకోకు",
                "మాటలాడవద్దు", "తప్పించు", "వదిలించు", "కలిపేయి", "పంపించేయి",
                "పంపించండి", "పంపించకపోతే", "ఇచ్చాడు", "ఇస్తారు", "తీసుకోండి", "తీసుకోరు",
                "కరెక్ట్", "సరిపోతుంది", "తప్పదు", "అవ్వాలి", "కావాలి", "కావలసిన",
                "కావచ్చు", "కావదు", "తప్పకండి", "అవకాశం", "సాధ్యం", "కుదరదు", "కుదిరితే",
                "కుదిరిందా", "ఏం చెప్పాలి", "చెప్పినట్టు", "చేయొచ్చు", "తినొచ్చు",
                "పోతారు", "చేస్తే బాగుంటుంది", "ఉండవచ్చు", "తినిపించు",
                "అనుకుంటున్నాను", "అనుకుంటున్నారు", "వెళ్ళిపో", "వస్తా", "వస్తే",
                "వెళ్ళిపోయాడు", "వెళ్ళిపోతాడు", "వెళ్ళిపోతున్నారు", "వచ్చిన",
                "తీసుకున్న", "చూడలేదు", "అనిపించకుండా", "అర్ధం కాలేదు", "తెలుసుకోలేరు",
                "గమనించలేరు",
                # Honorifics and Polite Particles
                "గారు", "జీ", "అయ్యా", "అక్కా", "చెప్పండి", "ఉండండి", "సర్", "మెడమ్",
                "అమ్మా", "నాన్న", "గురు",
                # Contextual and Discourse Markers
                "అంటారు", "అన్నాడు", "అంది", "వంటివి", "వంటి", "లాంటివి", "మరింత",
                "అనుకుంటే", "అనిపిస్తుంది", "అనిపించదు", "అంతేనా", "కాదా",
                "అప్పటికైతే", "ఇప్పటికైతే", "విషయంలో", "పరిస్థితిలో", "అర్థం",
                "తెలుసుకో", "విడిగా", "మొత్తానికి", "ఆఖరికి", "మొదట", "తర్వాతే",
                "ఇప్పుడే", "కానీనా", "అలానే", "చేయాలి", "చేయకపోతే", "తప్పదని",
                "కనిపిస్తే", "కనిపిస్తాడు", "కనిపిస్తుంది", "అలాంటివన్నీ",
                "ఇలాంటివన్నీ", "వాటన్నీ", "వాళ్లంతా", "మనుషులు", "ఆడవాళ్ళు",
                "మగవాళ్ళు", "ఇలాంటివారు", "అలాంటివారు", "ఇలాంటిదే", "అలాంటిదే",
                "పెద్దగా లేరు", "చిన్నగా లేదు",
                # Dialectal Variants and Slang
                "లే", "రా", "వా", "పో", "తిను", "అద్దిరిపోయింది", "సార్", "బాస్", "బాబు",
                "అమ్మాయ్", "అబ్బాయ్", "చూడు", "పోనీవు", "కలుపు", "పంపు", "వద్దురా",
                "ఓ",
                # Negations and Emphasis
                "ఏం కాదు", "కాదురా", "అసలు కాదు", "ఇంకాస్త", "ఎందుకు లేదో", "ఇలా కాదు",
                "ఇప్పుడు కాదు", "ఇప్పుడే కాదు", "ఎప్పుడైనా సరే", "ఎవరైనా సరే",
                "ఏమైనా సరే",
                # Code-Mixed Terms
                "అండ్", "ఓర్", "బట్", "ఇస్", "ఆర్", "ది", "ఏ", "అన్", "ఫర్", "టు", "ఇన్",
                "ఆట్", "విత్",
                # Punctuation
                ".", ",", "?", "!", ":", ";", "-", "_", "@", "#", "$", "%", "&", "*", "(", ")",
                "[", "]", "{", "}", "<", ">", "|", "\\", "/", "'", "\"", "```", "``"
            ],
            "english": [
                # Conjunctions
                "mariyu", "leda", "kani", "ayithe", "endukante", "kabatti", "anduvalla", "matram",
                "ayinappatiki", "kakapothe", "inka", "leka", "lekapothe", "tappa", "kani", "ante",
                "anduke", "ganuka", "alage", "ilane",
                # Pronouns
                "nenu", "meeru", "neevu", "atanu", "aame", "idi", "adi", "varu", "memu", "vallu",
                "ee", "aa", "evaru", "edi", "evaraina", "edaina", "evaru", "emi", "evaro", "edo",
                "tanu", "tam", "tana", "mana", "manaki", "manalo", "manavallu", "mee", "meeto",
                "meeda", "meeku", "naku", "nannu", "nanne", "maa", "tanaki", "tananu", "tanato",
                "tanapai", "dani", "danilo", "danivalla", "evariki", "evarito", "evarinaina",
                "itadu", "avi", "ivi", "vitini", "evi", "evaina", "inkevaru", "inka evaru",
                "inka emi", "entaina", "evadaina", "maa vaariki", "vallapai", "deenipai", "avida",
                "ayana",
                # Postpositions
                "lo", "pai", "ku", "nundi", "vadda", "to", "gurinchi", "madhya", "dwara", "kinda",
                "pakkana", "venta", "kosam", "lopal", "velupala", "vaipu", "daggara", "meeda",
                "krinda", "paina", "varaku", "valana", "kante",
                # Auxiliary Verbs
                "undi", "unnayi", "undu", "unnanu", "unnamu", "unnaru", "untundi", "untayi",
                "unte", "undi", "unna", "undali", "undadu", "undaga", "undevadu", "undevaru",
                "untunna", "avutundi", "avutanu", "avutaru", "ayindi",
                # Adverbs
                "ippudu", "appudu", "eppudu", "eppudaina", "ekkada", "ikkada", "akkada", "ela",
                "chala", "konta", "poortiga", "daadapu", "tvaralo", "ventane", "malli",
                "eppatiki", "eppatinundi", "enta", "ento", "ekkuvaga", "intavaraku",
                "ippatike", "ippativaraku", "appativaraku", "taruvata", "aa taruvata",
                "eppudayina", "eppatikaina", "ippatiki", "ippatikaina", "appatikappudu",
                "ippatikappudu", "kasepu", "intalo", "antalo", "peddaga", "chinnaga",
                "mari antaga", "mukhyanga", "sadharaṇanga", "appude", "intaku munde",
                "chala rojula taruvata", "konni rojula taruvata", "konni gantala taruvata",
                "konni nimishala taruvata",
                # Particles
                "kuda", "matrame", "asalu", "emo", "ani", "ante", "gani", "vanti", "lanti",
                "tappa", "okkasari", "kanuka", "ganuka",
                # Interjections
                "are", "oho", "ayyo", "hai", "o", "he", "abba", "chhi", "avunu", "kadu", "sare",
                "avuna", "avutunda", "chalu",
                # Quantifiers
                "anni", "konni", "prati", "e", "chala", "konchem", "ekkuva", "takkva", "aneka",
                "okati", "rendu", "moodu", "nalugu", "andaru", "anta", "ante", "inta", "inte",
                # Verbs (Common, Modal, Auxiliary)
                "vacche", "velle", "vellindi", "vacchindi", "tine", "tinna", "tinnanu", "tinatam",
                "vaddu", "vaccharu", "tirigi", "koodadanukunte", "vaddanukunte", "tinaledu",
                "tinna", "tinalenu", "vacchanu", "vellanu", "velleledu", "veltanu", "veltadu",
                "veltaru", "vastanu", "vastadu", "vastaru", "teesukura", "pampinchu", "teesuko",
                "ivvu", "teesukommu", "ivvandi", "vaddura", "vaddandi", "chesi", "chese",
                "chesina", "chestunna", "veltunna", "vastunna", "teera", "talapette", "talache",
                "chuste", "vinipistundi", "vinte", "chudali", "teliyadu", "telustundi", "unchu",
                "vadiliveyi", "pattinchukoku", "mataladavvaddu", "tappinchu", "vadilinch",
                "kalipeyi", "pampincheyi", "pampinchandi", "pampinchakapote", "icchadu",
                "istaru", "teesukondi", "teesukoru", "karekt", "saripotundi", "tappadu",
                "avvali", "kavali", "kavalasina", "kavacchu", "kavadu", "tappakandi",
                "avakasam", "sadhyam", "kudaradu", "kudirite", "kudirinda", "em cheppali",
                "cheppinattu", "cheyocchu", "tinocchu", "potaru", "cheste baguntundi",
                "undavacchu", "tinipinch", "anukuntunnanu", "anukuntunnaru", "vellipo",
                "vasta", "vaste", "vellipoyadu", "vellipotadu", "vellipotunnaru", "vacchina",
                "teesukunna", "chudaledu", "anipinchakunda", "ardham kaledu", "telusukoleru",
                "gamaninchaleru",
                # Honorifics and Polite Particles
                "garu", "jee", "ayya", "akka", "cheppandi", "undandi", "sar", "medam", "amma",
                "nanna", "guru",
                # Contextual and Discourse Markers
                "antaru", "annadu", "andi", "vantivi", "vanti", "lantivi", "marinta",
                "anukunte", "anipistundi", "anipinchadu", "antena", "kada", "appatikaite",
                "ippatikaite", "vishayambulo", "paristitilo", "artham", "telusuko", "vidiga",
                "mottaniki", "akhariki", "modata", "taruvate", "ippude", "kanina", "alane",
                "cheyali", "cheyakapothe", "tappadani", "kanipiste", "kanipistadu",
                "kanipistundi", "alantivanni", "ilantivanni", "vatanni", "vallanta", "manushulu",
                "adavallu", "magavallu", "ilantivaru", "alantivaru", "ilantide", "alantide",
                "peddaga leru", "chinnaga ledu",
                # Dialectal Variants and Slang
                "le", "ra", "va", "po", "tinu", "addripoyindi", "sar", "bas", "babu", "ammay",
                "abbay", "chudu", "poneevu", "kalupu", "pampu", "vaddura", "o",
                # Negations and Emphasis
                "em kadu", "kadura", "asalu kadu", "inkasta", "enduku ledo", "ila kadu",
                "ippudu kadu", "ippude kadu", "eppudaina sare", "evaraina sare", "emaina sare",
                # Code-Mixed Terms
                "and", "or", "but", "is", "are", "the", "a", "an", "for", "to", "in", "at", "with",
                # Punctuation
                ".", ",", "?", "!", ":", ";", "-", "_", "@", "#", "$", "%", "&", "*", "(", ")",
                "[", "]", "{", "}", "<", ">", "|", "\\", "/", "'", "\"", "```", "``"
            ]
        }

    def _telugu_sort_key(self, word: str) -> tuple:
        """Custom sorting key to prioritize Telugu script characters."""
        # Telugu Unicode range: \u0C00-\u0C7F
        is_telugu = any('\u0C00' <= char <= '\u0C7F' for char in word)
        return (not is_telugu, word.lower())

    def get_stopwords(self, script: str = "telugu", custom_stopwords: Optional[List[str]] = None) -> List[str]:
        """
        Get Telugu stopwords in specified script format.

        Args:
            script: Either 'telugu' for Telugu script or 'english' for transliterated words.
            custom_stopwords: Optional list of additional stopwords to include.

        Returns:
            List of stopwords sorted with Telugu script prioritized.

        Raises:
            ValueError: If script is not 'telugu' or 'english'.
        """
        if script not in ["telugu", "english"]:
            raise ValueError("Script must be either 'telugu' or 'english'")
        
        stopwords = self.stopwords[script][:]
        
        if custom_stopwords:
            stopwords.extend(custom_stopwords)
        
        return sorted(set(stopwords), key=self._telugu_sort_key)

    def add_stopwords(self, new_stopwords: List[str], script: str = "telugu") -> None:
        """
        Add new stopwords to the specified script.

        Args:
            new_stopwords: List of stopwords to add.
            script: Either 'telugu' or 'english'.

        Raises:
            ValueError: If script is not 'telugu' or 'english'.
        """
        if script not in ["telugu", "english"]:
            raise ValueError("Script must be either 'telugu' or 'english'")
        
        self.stopwords[script].extend(new_stopwords)
        self.stopwords[script] = sorted(set(self.stopwords[script]), key=self._telugu_sort_key)

    def remove_stopwords(self, stopwords_to_remove: List[str], script: str = "telugu") -> None:
        """
        Remove specified stopwords from the specified script.

        Args:
            stopwords_to_remove: List of stopwords to remove.
            script: Either 'telugu' or 'english'.

        Raises:
            ValueError: If script is not 'telugu' or 'english'.
        """
        if script not in ["telugu", "english"]:
            raise ValueError("Script must be either 'telugu' or 'english'")
        
        self.stopwords[script] = [sw for sw in self.stopwords[script] if sw not in stopwords_to_remove]

    def save_to_json(self, filename: str = "telugu_stopwords.json") -> None:
        """
        Save the stopwords to a JSON file.

        Args:
            filename: Name of the file to save stopwords to.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.stopwords, f, ensure_ascii=False, indent=4)
        print(f"Stopwords saved to {filename}")

    def load_from_json(self, filename: str = "telugu_stopwords.json") -> Dict[str, List[str]]:
        """
        Load stopwords from a JSON file.

        Args:
            filename: Name of the file to load stopwords from.

        Returns:
            Dictionary of stopwords.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.stopwords = json.load(f)
            print(f"Stopwords loaded from {filename}")
            return self.stopwords
        except FileNotFoundError:
            print(f"File {filename} not found. Using default stopwords.")
            return self.stopwords

def remove_stopwords(text: str, script: str = "telugu", custom_stopwords: Optional[List[str]] = None) -> str:
    """
    Remove Telugu stopwords from text.

    Args:
        text: Text to process.
        script: Either 'telugu' for Telugu script or 'english' for transliterated words.
        custom_stopwords: Optional list of additional stopwords to include.

    Returns:
        Text with stopwords removed.
    """
    telugu_sw = TeluguStopWords()
    stopwords = telugu_sw.get_stopwords(script, custom_stopwords)
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return " ".join(filtered_words)

if __name__ == "__main__":
    telugu_sw = TeluguStopWords()
    telugu_stopwords = telugu_sw.get_stopwords(script="telugu")
    print(f"First 5 Telugu stopwords: {telugu_stopwords[:5]}")
    sample_text = "నేను ఈ రోజు చాలా సంతోషంగా ఉన్నాను కాబట్టి నేను బయటకు వెళ్లాలనుకుంటున్నాను"
    cleaned_text = remove_stopwords(sample_text)
    print(f"Original: {sample_text}")
    print(f"Cleaned: {cleaned_text}")
    # Added a comment for CI/CD testing