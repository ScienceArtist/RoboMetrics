"""
Enhanced Robot Framework Test Analysis Tool
Credits: @ScienceArtist (GitHub)
Features:
- Test complexity analysis using Shannon Entropy
- Redundancy detection using Jaccard Similarity
- Keyword usage patterns
- Test suite structure analysis
"""

import sys
import json
import math
import ast
import os
from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple
from datetime import datetime

class RobotTestAnalyzer:
    def __init__(self, test_dir: str):
        self.test_dir = test_dir
        self.test_cases = []
        self.keyword_usage = defaultdict(int)
        self.suite_structure = defaultdict(list)

    def get_function_body(self, node: ast.FunctionDef) -> List[str]:
        """Extract function body as list of strings."""
        body_lines = []
        for stmt in node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Str):
                # Skip docstrings
                continue
            # Get the line numbers for this statement
            start_line = stmt.lineno
            try:
                end_line = stmt.end_lineno if hasattr(stmt, 'end_lineno') else start_line
            except:
                end_line = start_line
            
            body_lines.append(f"Line {start_line}-{end_line}")
        return body_lines

    def extract_robot_keywords(self, file_path: str) -> List[Dict]:
        """Extract Robot Framework keywords from a Python file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            keywords = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Look for Robot Framework keyword pattern (functions with robot_keyword decorator)
                    is_keyword = False
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                            is_keyword = True
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                is_keyword = True
                    
                    if is_keyword or node.name.startswith('test_'):
                        keyword_info = {
                            "name": node.name,
                            "lineno": node.lineno,
                            "file": file_path,
                            "args": [arg.arg for arg in node.args.args if arg.arg != 'self'],
                            "body": self.get_function_body(node)
                        }
                        keywords.append(keyword_info)
                        self.keyword_usage[node.name] += 1
            
            return keywords
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {str(e)}")
            return []

    def analyze_test_complexity(self) -> List[Dict]:
        """Calculate complexity scores for each test case."""
        complexity_scores = []
        for test in self.test_cases:
            steps = len(test["body"])
            # Calculate Shannon entropy based on keyword usage
            entropy = 0
            if steps > 0:
                step_counts = Counter(test["body"])
                for count in step_counts.values():
                    p = count / steps
                    entropy -= p * math.log2(p)
            
            complexity_scores.append({
                "Test Keyword": test["name"],
                "Entropy Score": round(entropy, 2),
                "Step Count": steps
            })
        
        return sorted(complexity_scores, key=lambda x: x["Entropy Score"], reverse=True)

    def find_redundant_tests(self) -> List[Dict]:
        """Find potentially redundant tests using Jaccard similarity."""
        redundant_pairs = []
        for i, test1 in enumerate(self.test_cases):
            for test2 in self.test_cases[i+1:]:
                steps1 = set(test1["body"])
                steps2 = set(test2["body"])
                
                intersection = len(steps1.intersection(steps2))
                union = len(steps1.union(steps2))
                
                if union > 0:
                    similarity = intersection / union
                    if similarity > 0.8:  # 80% similarity threshold
                        redundant_pairs.append({
                            "test1": test1["name"],
                            "test2": test2["name"],
                            "similarity": round(similarity, 2)
                        })
        
        return sorted(redundant_pairs, key=lambda x: x["similarity"], reverse=True)

    def analyze_keyword_patterns(self) -> Dict:
        """Analyze keyword usage patterns."""
        return {
            "most_used_keywords": dict(Counter(self.keyword_usage).most_common(10)),
            "unused_keywords": [k for k, v in self.keyword_usage.items() if v == 0]
        }

    def analyze(self) -> Dict:
        # Process all Python files in the directory
        for root, _, files in os.walk(self.test_dir):
            for filename in files:
                if filename.endswith(".py"):
                    file_path = os.path.join(root, filename)
                    extracted_tests = self.extract_robot_keywords(file_path)
                    if extracted_tests:
                        self.test_cases.extend(extracted_tests)
                        self.suite_structure[os.path.basename(root)].extend(extracted_tests)

        if not self.test_cases:
            raise ValueError("No Robot Framework keywords found in the given directory.")

        # Generate comprehensive report
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "test_suite_summary": {
                "total_tests": len(self.test_cases),
                "total_keywords": len(self.keyword_usage),
                "total_suites": len(self.suite_structure)
            },
            "complexity_analysis": self.analyze_test_complexity(),
            "redundancy_analysis": self.find_redundant_tests(),
            "keyword_patterns": self.analyze_keyword_patterns(),
            "suite_structure": {
                suite: [test["name"] for test in tests]
                for suite, tests in self.suite_structure.items()
            }
        }
        
        # Save report to file
        os.makedirs(os.path.join(self.test_dir, "test_analysis_output"), exist_ok=True)
        report_path = os.path.join(self.test_dir, "test_analysis_output", "analysis_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)

        return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py <directory_with_robot_libraries>")
        sys.exit(1)

    try:
        analyzer = RobotTestAnalyzer(sys.argv[1])
        report = analyzer.analyze()
        print(json.dumps(report, indent=4))
        print(f"\nAnalysis complete. Report saved in: {os.path.join(sys.argv[1], 'test_analysis_output')}")
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()