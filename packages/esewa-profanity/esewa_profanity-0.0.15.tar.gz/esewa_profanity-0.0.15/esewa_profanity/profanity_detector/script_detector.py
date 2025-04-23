import json

class ScriptDetector:
    def load_script_range(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
        return {script: (int(start, 16), int(end, 16)) for script, (start, end) in raw_data.items()}
    
    def detect_script_from_json(self,text, script_ranges):
        script_counts = {script: 0 for script in script_ranges}

        for char in text:
            code_point = ord(char)
            for script, (start, end) in script_ranges.items():
                if start <= code_point <= end:
                    script_counts[script] += 1

        detected = [s for s, c in script_counts.items() if c > 0]
        return detected or ['Unknown']
    
    def detect(self, file_location, text):
        script_range = self.load_script_range(file_location)
        # print(script_range)
        return self.detect_script_from_json(text=text,script_ranges=script_range)[0]
    
if __name__=="__main__":
    detector = ScriptDetector()
    detector.detect()