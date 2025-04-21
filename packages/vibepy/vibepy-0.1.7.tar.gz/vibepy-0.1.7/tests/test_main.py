import pytest
from unittest.mock import patch, MagicMock
import sys
from vibepy.main import main
from readchar import key

@pytest.fixture
def mock_openai():
    with patch('vibepy.main.openai') as mock:
        # Mock the client and its methods to prevent any API calls
        mock_client = MagicMock()
        mock.ChatCompletion.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test response"))]
        )
        # Mock any potential authentication errors
        mock.OpenAIError = Exception
        mock.AuthenticationError = Exception
        mock.APIError = Exception
        # Mock the client to prevent any actual API calls
        mock.Client.return_value = mock_client
        yield mock

@pytest.fixture
def mock_readchar():
    with patch('vibepy.main.readkey') as mock:
        yield mock

@pytest.fixture
def mock_pyperclip():
    with patch('vibepy.main.pyperclip') as mock:
        yield mock

@pytest.fixture
def mock_colorama():
    with patch('vibepy.main.init'), patch('vibepy.main.Fore') as mock_fore:
        mock_fore.GREEN = "GREEN"
        mock_fore.YELLOW = "YELLOW"
        mock_fore.CYAN = "CYAN"
        mock_fore.RED = "RED"
        yield mock_fore

def test_main_with_openai(mock_openai, mock_readchar, mock_pyperclip, mock_colorama, capsys):
    # Mock readkey to simulate UP key press, then ESC
    mock_readchar.side_effect = [key.UP, key.ESC]
    
    # Mock input to return test code
    with patch('builtins.input', return_value="print('hello')"):
        main()
    
    captured = capsys.readouterr()
    assert "Welcome to Vibepy!" in captured.out
    assert "Test response" in captured.out

def test_main_without_openai(mock_readchar, mock_pyperclip, mock_colorama, capsys):
    # Mock readkey to simulate UP key press, then ESC
    mock_readchar.side_effect = [key.UP, key.ESC]
    
    # Mock input to return test code
    with patch('builtins.input', return_value="print('hello')"):
        # Remove openai from sys.modules to simulate it not being installed
        with patch.dict('sys.modules', {'openai': None}):
            main()
    
    captured = capsys.readouterr()
    assert "Welcome to Vibepy!" in captured.out
    assert "AI features require the 'openai' package" in captured.out

def test_main_run_mode(mock_readchar, mock_pyperclip, mock_colorama, capsys):
    # Mock readkey to simulate UP key press, then ESC
    mock_readchar.side_effect = [key.UP, key.ESC]
    
    # Mock input to return test code
    with patch('builtins.input', return_value="print('hello')"):
        # Mock sys.argv to include --run=True
        with patch('sys.argv', ['vibepy', '--run=True']):
            main()
    
    captured = capsys.readouterr()
    assert "Welcome to Vibepy!" in captured.out
    assert "hello" in captured.out 