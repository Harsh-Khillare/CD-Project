#!/usr/bin/env python
"""Demo script - Shows AI Error Tutor in action"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from error_generator import CErrorGenerator, PythonErrorGenerator, ErrorDataset
from error_context import CContextExtractor, PythonContextExtractor
from security_guard import SecurityGuard
from dataset import DataPreprocessor

def print_section(title):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def demo_c_errors():
    """Demonstrate C error generation and explanation"""
    print_section("DEMO 1: C Error Generation and Analysis")
    
    # Generate errors
    errors = [
        CErrorGenerator.undefined_variable("sum", 5),
        CErrorGenerator.missing_semicolon(4),
        CErrorGenerator.type_mismatch("x", "int", "char*"),
        CErrorGenerator.missing_header("math.h"),
    ]
    
    for i, error in enumerate(errors, 1):
        print(f"Error {i}: {error.error_type.upper()}")
        print(f"  Message: {error.original_message}")
        print(f"  Line: {error.line_number}")
        print(f"  Explanation: {error.explanation}")
        print()

def demo_python_errors():
    """Demonstrate Python error generation"""
    print_section("DEMO 2: Python Error Generation and Analysis")
    
    # Generate errors
    errors = [
        PythonErrorGenerator.name_error("total"),
        PythonErrorGenerator.indentation_error(),
        PythonErrorGenerator.type_error(),
        PythonErrorGenerator.attribute_error(),
    ]
    
    for i, error in enumerate(errors, 1):
        print(f"Error {i}: {error.error_type.upper()}")
        print(f"  Message: {error.original_message}")
        print(f"  Explanation: {error.explanation}")
        print()

def demo_context_extraction():
    """Demonstrate context extraction"""
    print_section("DEMO 3: Error Context Extraction")
    
    c_code = """#include <stdio.h>

int main() {
    int x = 5;
    int y = x + 10;  // Error on this line
    printf("%d\\n", y);
    return 0;
}"""
    
    print("C Code Context Extraction:")
    print("Code:")
    print(c_code)
    print()
    
    context = CContextExtractor.extract_context(c_code, 5)
    print(f"Available variables: {context.available_variables}")
    print(f"Function context: {context.function_context}")
    print(f"Includes: {context.imports}")
    print()
    
    python_code = """def calculate(a, b):
    result = a + b
    return result

x = calculate(5, 10)
print(x)
"""
    
    print("\nPython Code Context Extraction:")
    print("Code:")
    print(python_code)
    print()
    
    context = PythonContextExtractor.extract_context(python_code, 3)
    print(f"Function context: {context.function_context}")
    print(f"Available variables: {context.available_variables}")

def demo_security_analysis():
    """Demonstrate security checking"""
    print_section("DEMO 4: Security Analysis")
    
    test_cases = [
        ("int x = 5; int y = x + 10;", "c", True),
        ("strcpy(dest, src);", "c", False),
        ("gets(buffer);", "c", False),
        ("result = a + b", "python", True),
        ("eval(user_input)", "python", False),
        ("pickle.loads(data)", "python", False),
    ]
    
    for code, language, expected_safe in test_cases:
        is_safe, reason = SecurityGuard.is_safe(code, language)
        status = "✓ SAFE" if is_safe else "✗ UNSAFE"
        print(f"{status} ({language}): {code}")
        if not is_safe:
            print(f"       Reason: {reason}")
        print()

def demo_text_preprocessing():
    """Demonstrate text preprocessing"""
    print_section("DEMO 5: Text Preprocessing and Simplification")
    
    messages = [
        "UNDEFINED REFERENCE to `main'",
        "implicit declaration of function `printf'",
        "incompatible types when assigning to type 'int' from type 'char *'",
    ]
    
    print("Original Messages:")
    for msg in messages:
        print(f"  - {msg}")
    
    print("\nNormalized Messages:")
    for msg in messages:
        normalized = DataPreprocessor.normalize_error_message(msg)
        print(f"  - {normalized}")
    
    print("\n\nExplanation Simplification:")
    explanation = "uninitialized variable causing segmentation fault and buffer overflow"
    print(f"Original: {explanation}")
    simplified = DataPreprocessor.simplify_explanation_for_beginners(explanation)
    print(f"Simplified: {simplified}")

def demo_dataset_generation():
    """Demonstrate dataset generation"""
    print_section("DEMO 6: Dataset Generation")
    
    dataset = ErrorDataset()
    errors = dataset.generate_default_dataset()
    
    print(f"Generated dataset with {len(errors)} errors")
    print(f"\nError type distribution:")
    
    type_counts = {}
    for error in errors:
        error_type = error.error_type
        type_counts[error_type] = type_counts.get(error_type, 0) + 1
    
    for error_type, count in sorted(type_counts.items()):
        percentage = (count / len(errors)) * 100
        print(f"  {error_type}: {count} ({percentage:.1f}%)")

def main():
    """Run all demonstrations"""
    print("\n" + "="*70)
    print("AI ERROR TUTOR - DEMONSTRATION".center(70))
    print("="*70)
    
    try:
        demo_c_errors()
        demo_python_errors()
        demo_context_extraction()
        demo_security_analysis()
        demo_text_preprocessing()
        demo_dataset_generation()
        
        print_section("DEMO COMPLETED")
        print("✓ All demonstrations completed successfully!")
        print("\nNext steps:")
        print("  1. Generate training dataset: python main.py generate-dataset")
        print("  2. Train the model: python main.py train")
        print("  3. Test model: python main.py test-model")
        print("  4. Explain errors: python main.py explain your_file.c")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
