import pytest
import readchar
import os
from unittest.mock import patch, MagicMock
from vibepy.cli import main, run_vibepy

def test_run_vibepy():
    """Test the run_vibepy function with different run parameters."""
    # Skip if OpenAI API key is not available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    with patch('subprocess.run') as mock_run:
        # Test with run=False
        run_vibepy(run=False)
        mock_run.assert_called_once_with(["python", "vibepy.py", "--run", "False"])
        
        # Reset mock and test with run=True
        mock_run.reset_mock()
        run_vibepy(run=True)
        mock_run.assert_called_once_with(["python", "vibepy.py", "--run", "True"])

@pytest.mark.parametrize("input_sequence,expected_outputs", [
    # Test ESC key to exit immediately
    ([readchar.key.ESC], ["Press ↑ to initiate vibepy", "Press ESC to exit", "Exiting..."]),
    
    # Test UP arrow followed by ESC
    ([readchar.key.UP, readchar.key.ESC], [
        "Press ↑ to initiate vibepy",
        "Press ESC to exit",
        "Vibepy initiated!",
        "Press - for REPL mode (--run FALSE)",
        "Press = for execution mode (--run TRUE)",
        "Press ESC to exit",
        "Exiting vibepy..."
    ]),
    
    # Test UP arrow followed by - (REPL mode)
    ([readchar.key.UP, "-"], [
        "Press ↑ to initiate vibepy",
        "Press ESC to exit",
        "Vibepy initiated!",
        "Press - for REPL mode (--run FALSE)",
        "Press = for execution mode (--run TRUE)",
        "Press ESC to exit",
        "Entering REPL mode..."
    ]),
    
    # Test UP arrow followed by = (execution mode)
    ([readchar.key.UP, "="], [
        "Press ↑ to initiate vibepy",
        "Press ESC to exit",
        "Vibepy initiated!",
        "Press - for REPL mode (--run FALSE)",
        "Press = for execution mode (--run TRUE)",
        "Press ESC to exit",
        "Entering execution mode..."
    ]),
])
def test_main_hotkeys(input_sequence, expected_outputs, capsys):
    """Test the main function with different key sequences."""
    # Skip if OpenAI API key is not available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    with patch('readchar.readkey', side_effect=input_sequence):
        with patch('vibepy.cli.run_vibepy') as mock_run_vibepy:
            try:
                main()
            except StopIteration:
                pass  # Expected when we run out of input sequence
            
            # Get the captured output
            captured = capsys.readouterr()
            output_lines = captured.out.split('\n')
            
            # Check that all expected outputs appear in the actual output
            for expected in expected_outputs:
                assert any(expected in line for line in output_lines), f"Expected output '{expected}' not found"
            
            # Verify run_vibepy was called appropriately
            if "-" in input_sequence:
                mock_run_vibepy.assert_called_once_with(run=False)
            elif "=" in input_sequence:
                mock_run_vibepy.assert_called_once_with(run=True)
            else:
                mock_run_vibepy.assert_not_called()

def test_invalid_key():
    """Test handling of invalid keys after initialization."""
    # Skip if OpenAI API key is not available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    with patch('readchar.readkey', side_effect=[readchar.key.UP, "x", readchar.key.ESC]):
        with patch('vibepy.cli.run_vibepy') as mock_run_vibepy:
            with patch('builtins.print') as mock_print:
                try:
                    main()
                except StopIteration:
                    pass
                
                # Verify that invalid key message was printed
                mock_print.assert_any_call("\nInvalid key. Press - for REPL mode, = for execution mode, or ESC to exit")
                mock_run_vibepy.assert_not_called()

def test_main():
    """Test the main function with different command line arguments."""
    test_cases = [
        (["vibepy", "--run", "False"], False),
        (["vibepy", "--run", "True"], True),
        (["vibepy"], False)
    ]
    
    for args, expected_run in test_cases:
        with patch('sys.argv', args):
            with patch('vibepy.cli.run_vibepy') as mock_run_vibepy:
                main()
                mock_run_vibepy.assert_called_once_with(run=expected_run)

def test_main_help():
    """Test that --help flag works without initializing the full application."""
    with patch('sys.argv', ["vibepy", "--help"]):
        with patch('argparse.ArgumentParser.print_help') as mock_print_help:
            main()
            mock_print_help.assert_called_once() 