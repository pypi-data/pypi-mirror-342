import os
import logging
from scorer.payloadreader import GraderPayloadReader
from scorer.preprocesser import GraderPreprocessor
from scorer.comparator import GraderComparator
from scorer.configs import GraderConfigs

grader_configs = GraderConfigs()

class GraderComponent:
    def read_input_payload(self, file: bytes, filename: str, role_code: str):
        try:
            # Step 1: Read file content based on extension
            extension = filename.split('.')[-1].lower()
            if extension == 'pdf':
                raw_text = GraderPayloadReader.read_pdf(file)
            elif extension == 'docx':
                raw_text = GraderPayloadReader.read_docx(file)
            else:
                raise ValueError("Unsupported file type")

            # Step 2: Preprocess text
            processed_text = GraderPreprocessor().preprocess(raw_text)

            # Step 3: Fetch keywords from the corresponding .txt file based on role_code
            if not role_code:
                raise ValueError("role_code is missing in input")

            role_to_file = {
                'pd': 'pd_keywords.txt',
                'jd': 'jd_keywords.txt',
                'pfd': 'pfd_keywords.txt',
                'jfd': 'jfd_keywords.txt'
            }

            keywords_file = role_to_file.get(role_code.lower())
            if not keywords_file:
                raise ValueError(f"No keywords file mapping for role_code: {role_code}")
                
            script_dir = os.path.dirname(__file__)
            base_dir = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
            config_dir = os.path.join(base_dir, 'fytly', 'configs')
            file_path = os.path.join(config_dir, keywords_file)

            print(f"Looking for file at: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    raise ValueError(f"Keywords file {keywords_file} is empty")
                pairs = content.split(',')
                keywords_result = {pair.split(':')[0].strip(): int(pair.split(':')[1]) for pair in pairs if ':' in pair}

            print(f"processed_text type: {type(processed_text)}, value: {processed_text[:50]}...")
            print(f"keywords_result type: {type(keywords_result)}, value: {keywords_result}")

            # Step 4: Compare resume to role
            comparison_result = GraderComparator().compare_resume_to_role(processed_text, keywords_result)

            if not isinstance(comparison_result, dict):
                raise TypeError("compare_resume_to_role must return a dictionary")

            print(f"comparison_result type: {type(comparison_result)}, value: {comparison_result}")

            total_score = comparison_result.get("total_score", 0)
            matched_keywords = comparison_result.get("matched_keywords", [])

            # Step 5: Eligibility logic
            backend_developer_score = int(grader_configs.props.get('backend_developer_score'))
            full_stack_developer_score = int(grader_configs.props.get('full_stack_developer_score'))
            eligible = False
            message = "Not eligible"

            if role_code.lower() in ['pd', 'jd'] and total_score >= backend_developer_score:
                eligible = True
                message = "Eligible for this role"
            elif role_code.lower() in ['pfd', 'jfd'] and total_score >= full_stack_developer_score:
                eligible = True
                message = "Eligible for this role"

            return {
                "role_code": role_code,
                "comparator_score": total_score,
                "matched_keywords": matched_keywords,
                "eligible": eligible,
                "message": message
            }

        except Exception as e:
            logging.error(f"read input payload failed: {e}")
            raise
