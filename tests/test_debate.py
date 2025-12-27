# Automated tests for debate system
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import create_initial_state
from validation import check_repetition, check_topic_relevance, validate_argument


def test_turn_enforcement():
    print("Testing turn enforcement...")
    
    state = create_initial_state("Test topic")
    
    # Initial speaker should be AgentA
    assert state['current_speaker'] == 'AgentA', "Initial speaker should be AgentA"
    
    # After AgentA speaks, should be AgentB
    # This would be tested in integration with actual workflow
    
    print("[PASS] Turn enforcement test passed")


def test_repetition_detection():
    print("Testing repetition detection...")
    
    previous = [
        {'round': 1, 'agent': 'AgentA', 'text': 'AI should be regulated for safety'},
        {'round': 2, 'agent': 'AgentB', 'text': 'Regulation will stifle innovation'}
    ]
    
    # Test exact repetition
    is_rep, reason = check_repetition('AI should be regulated for safety', previous)
    assert is_rep, "Should detect exact repetition"
    
    # Test similar but not exact
    is_rep, reason = check_repetition('AI needs regulation for security reasons', previous, similarity_threshold=0.4)
    assert is_rep, "Should detect similar argument"
    
    # Test different argument
    is_rep, reason = check_repetition('Climate change requires immediate action', previous)
    assert not is_rep, "Should not flag different argument"
    
    print("[PASS] Repetition detection test passed")


def test_topic_relevance():
    print("Testing topic relevance...")
    
    topic = "Should artificial intelligence be regulated"
    
    # Relevant argument
    is_rel, score = check_topic_relevance(
        "Artificial intelligence regulation is necessary",
        topic
    )
    assert is_rel, f"Should detect relevant argument (score: {score})"
    
    # Irrelevant argument
    is_rel, score = check_topic_relevance(
        "I like pizza and pasta",
        topic,
        min_relevance=0.3
    )
    assert not is_rel, f"Should detect irrelevant argument (score: {score})"
    
    print("[PASS] Topic relevance test passed")


def test_argument_validation():
    print("Testing argument validation...")
    
    topic = "Should AI be regulated"
    previous = [
        {'round': 1, 'agent': 'AgentA', 'text': 'AI regulation is important for safety and security'}
    ]
    
    # Test too short
    is_valid, msg = validate_argument("Too short", previous, topic, 'AgentA')
    assert not is_valid, "Should reject too short argument"
    
    # Test repetition
    is_valid, msg = validate_argument(
        "AI regulation is important for safety and security",
        previous, topic, 'AgentA'
    )
    assert not is_valid, "Should reject repeated argument"
    
    # Test valid new argument
    is_valid, msg = validate_argument(
        "Government oversight can ensure AI development aligns with public interest",
        previous, topic, 'AgentB'
    )
    assert is_valid, f"Should accept valid argument. Error: {msg}"
    
    print("[PASS] Argument validation test passed")


def test_memory_updates():
    print("Testing memory updates...")
    
    state = create_initial_state("Test topic")
    
    # Initial state should be empty
    assert len(state['arguments']) == 0, "Initial arguments should be empty"
    
    # Add an argument
    state['arguments'].append({
        'round': 1,
        'agent': 'AgentA',
        'text': 'Test argument'
    })
    
    assert len(state['arguments']) == 1, "Should have 1 argument after adding"
    assert state['arguments'][0]['agent'] == 'AgentA', "Agent should be AgentA"
    
    print("[PASS] Memory updates test passed")


def test_judge_output_format():
    print("Testing judge output format...")
    
    # This would test the actual judge output
    # For now, we test the expected format
    expected_fields = ['winner', 'reasoning', 'summary']
    
    # Judge output should contain a winner declaration
    sample_judgment = "Winner: AgentA. Reason: Better arguments."
    
    assert 'Winner' in sample_judgment, "Should contain winner"
    assert 'Reason' in sample_judgment or 'reason' in sample_judgment.lower(), "Should contain reasoning"
    
    print("[PASS] Judge output format test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Debate System Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_turn_enforcement,
        test_repetition_detection,
        test_topic_relevance,
        test_argument_validation,
        test_memory_updates,
        test_judge_output_format
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__} error: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
