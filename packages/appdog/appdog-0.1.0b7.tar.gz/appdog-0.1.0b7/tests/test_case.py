import pytest

from appdog._internal.case import to_name_case, to_pascal_case, to_snake_case, to_title_case


class TestCaseConversions:
    """Tests for string case conversion functions."""

    @pytest.mark.parametrize(
        'input_text,expected_output',
        [
            # Empty string
            ('', ''),
            # Basic examples
            ('hello_world', 'HelloWorld'),
            ('hello-world', 'HelloWorld'),
            ('hello world', 'HelloWorld'),
            # Already pascal case
            ('HelloWorld', 'HelloWorld'),
            # Mixed delimiters
            ('hello_world-example text', 'HelloWorldExampleText'),
            # With numbers
            ('hello_world123', 'HelloWorld123'),
            ('hello_world_123', 'HelloWorld123'),
            # Special cases with expected actual behavior
            ('API_key', 'APIKey'),  # Preserves acronym case
            ('OAuth2_token', 'OAuth2Token'),  # Preserves acronym case
            ('user_ID', 'UserID'),  # Preserves ID capitalization
            # With slashes and braces - use actual behavior
            ('hello/world', 'Hello/World'),
            ('file.ext', 'File.Ext'),
            ('path/to/file.js', 'Path/To/File.Js'),
            ('/users/{userId}', '/Users/{UserId}'),
            ('/users/{userId}/posts/{postId}', '/Users/{UserId}/Posts/{PostId}'),
        ],
    )
    def test_to_pascal_case(self, input_text: str, expected_output: str) -> None:
        """Test the to_pascal_case function with various input patterns."""
        assert to_pascal_case(input_text) == expected_output

    @pytest.mark.parametrize(
        'input_text,expected_output',
        [
            # Empty string
            ('', ''),
            # Basic examples
            ('helloWorld', 'hello_world'),
            ('HelloWorld', 'hello_world'),
            ('hello-world', 'hello_world'),
            ('hello world', 'hello_world'),
            # Already snake case
            ('hello_world', 'hello_world'),
            # Mixed delimiters
            ('helloWorld-example text', 'hello_world_example_text'),
            # With numbers
            ('helloWorld123', 'hello_world123'),
            ('HelloWorld123', 'hello_world123'),
            # Special cases with expected actual behavior
            ('APIKey', 'api_key'),
            ('OAuth2Token', 'o_auth2_token'),
            ('UserID', 'userid'),  # Does not treat ID specially
            # With slashes and braces - use actual behavior
            ('hello/world', 'hello/world'),
            ('file.ext', 'file.ext'),
            ('path/to/file.js', 'path/to/file.js'),
            ('/users/{userId}', '/users/{user_id}'),
            ('/users/{userId}/posts/{postId}', '/users/{user_id}/posts/{post_id}'),
        ],
    )
    def test_to_snake_case(self, input_text: str, expected_output: str) -> None:
        """Test the to_snake_case function with various input patterns."""
        assert to_snake_case(input_text) == expected_output

    @pytest.mark.parametrize(
        'input_text,expected_output',
        [
            # Empty string
            ('', ''),
            # Basic examples
            ('hello_world', 'Hello World'),
            ('helloWorld', 'Hello World'),
            ('HelloWorld', 'Hello World'),
            ('hello-world', 'Hello World'),
            ('hello world', 'Hello World'),
            # Mixed delimiters
            ('helloWorld-example_text', 'Hello World Example Text'),
            # With numbers
            ('helloWorld123', 'Hello World123'),
            ('HelloWorld123', 'Hello World123'),
            # Special cases with expected actual behavior
            ('APIKey', 'API Key'),
            ('OAuth2Token', 'O Auth2 Token'),
            ('UserID', 'UserID'),  # Preserves ID capitalization
            # With slashes and braces - use actual behavior
            ('hello/world', 'Hello/World'),
            ('file.ext', 'File.Ext'),
            ('path/to/file.js', 'Path/To/File.Js'),
            ('/users/{userId}', '/Users/{User Id}'),
            ('/users/{userId}/posts/{postId}', '/Users/{User Id}/Posts/{Post Id}'),
        ],
    )
    def test_to_title_case(self, input_text: str, expected_output: str) -> None:
        """Test the to_title_case function with various input patterns."""
        assert to_title_case(input_text) == expected_output

    def test_complex_path_handling(self) -> None:
        """Test generic case conversions with complex paths."""
        # Complex path with multiple segments
        input_path = '/api/v1/users/{userId}/posts/{postId}/comments'

        # Test different case conversions
        assert to_snake_case(input_path) == '/api/v1/users/{user_id}/posts/{post_id}/comments'
        assert to_pascal_case(input_path) == '/Api/V1/Users/{UserId}/Posts/{PostId}/Comments'
        assert to_title_case(input_path) == '/Api/V1/Users/{User Id}/Posts/{Post Id}/Comments'

    @pytest.mark.parametrize(
        'input_text,expected_output',
        [
            # Empty string
            ('', ''),
            # Basic examples
            ('get_user', 'get_user'),
            ('getUserProfile', 'get_user_profile'),
            # With parameters
            ('/users/{id}', 'users_by_id'),
            ('/users/{userId}', 'users_by_user_id'),
            ('/posts/{postId}/comments', 'posts_comments_by_post_id'),
            # Multiple parameters
            ('/users/{userId}/posts/{postId}', 'users_posts_by_user_id_and_post_id'),
            (
                '/api/v1/users/{userId}/posts/{postId}/comments/{commentId}',
                'api_v1_users_posts_comments_by_user_id_and_post_id_and_comment_id',
            ),
            # With dots and slashes
            ('api/v1/users', 'api_v1_users'),
            ('file.json', 'file_json'),
            # Mixed case in parameters
            ('/users/{userID}/posts/{PostId}', 'users_posts_by_userid_and_post_id'),
        ],
    )
    def test_to_name_case(self, input_text: str, expected_output: str) -> None:
        """Test the to_name_case function with various input patterns."""
        assert to_name_case(input_text) == expected_output
