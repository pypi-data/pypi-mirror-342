import logging
import re
from scorer.configs import GraderConfigs
from rapidfuzz import fuzz

grader_configs = GraderConfigs()

class GraderComparator:
    def compare_resume_to_role(self, resume_text, role_keywords):
        """
        Compare resume with role keywords and return:
        - total score based on matched weights
        - list of matched keywords from role

        Args:
            resume_text (str): The resume content
            role_keywords (dict): {keyword: weight}

        Returns:
            dict: {
                'total_score': int,
                'matched_keywords': list of strings
            }
        """
        try:
            threshold = int(grader_configs.props.get('threshold', 85))  # Default threshold 85

            if not resume_text or not role_keywords:
                logging.warning("Empty resume or keywords input.")
                return {"total_score": 0, "matched_keywords": []}

            # Extract words from resume
            words = re.findall(r'\b\w+\b', resume_text.lower())
            resume_words = set(words)  # Skip spell check for performance

            total_score = 0
            matched_keywords = []

            for keyword, weight in role_keywords.items():
                keyword = keyword.strip().lower()

                # Exact match first
                if keyword in resume_words:
                    total_score += weight
                    matched_keywords.append(keyword)
                    continue

                # Fuzzy match only if no exact match
                for word in resume_words:
                    score = fuzz.ratio(keyword, word)
                    if score >= threshold:
                        total_score += weight
                        matched_keywords.append(keyword)
                        break

            return {
                "total_score": total_score,
                "matched_keywords": matched_keywords
            }

        except Exception as e:
            logging.error(f"Comparison failed: {e}")
            raise
