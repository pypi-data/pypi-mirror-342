"""Tests for the Act manager."""

from unittest.mock import MagicMock

import pytest

from sologm.core.act import ActManager
from sologm.core.game import GameManager
from sologm.core.scene import SceneManager
from sologm.utils.errors import GameError


class TestActManager:
    """Tests for the ActManager class."""

    def test_manager_relationships(self, db_session, act_manager):
        """Test manager relationships."""
        # Test game_manager property
        assert isinstance(act_manager.game_manager, GameManager)

        # Test scene_manager property
        assert isinstance(act_manager.scene_manager, SceneManager)

        # Test passing explicit game_manager
        mock_game_manager = MagicMock(spec=GameManager)
        from sologm.core.act import ActManager

        act_manager_with_parent = ActManager(
            game_manager=mock_game_manager, session=db_session
        )
        assert act_manager_with_parent.game_manager is mock_game_manager

        # Test session is passed correctly
        assert act_manager_with_parent._session is db_session

    def test_create_act(self, db_session, test_game, act_manager):
        """Test creating an act."""
        # Create an act with title and summary
        act = act_manager.create_act(
            game_id=test_game.id,
            title="Test Act",
            summary="A test act",
        )

        assert act.id is not None
        assert act.game_id == test_game.id
        assert act.title == "Test Act"
        assert act.summary == "A test act"
        assert act.sequence == 1
        assert act.is_active is True

        # Complete the first act before creating a new one
        act_manager.complete_act(act_id=act.id)

        # Create an untitled act
        untitled_act = act_manager.create_act(
            game_id=test_game.id,
        )

        assert untitled_act.id is not None
        assert untitled_act.game_id == test_game.id
        assert untitled_act.title is None
        assert untitled_act.summary is None
        assert untitled_act.sequence == 2
        assert untitled_act.is_active is True

        # Refresh the first act to see if it was deactivated
        db_session.refresh(act)
        assert act.is_active is False  # Previous act should be deactivated

        # Test creating an act with make_active=False
        non_active_act = act_manager.create_act(
            game_id=test_game.id,
            title="Non-active Act",
            summary="This act won't be active",
            make_active=False,
        )

        assert non_active_act.id is not None
        assert non_active_act.is_active is False

        # Verify the previous act is still active
        db_session.refresh(untitled_act)
        assert untitled_act.is_active is True

    def test_create_act_with_context(self, session_context, test_game, act_manager):
        """Test creating an act using session context."""
        with session_context as session:
            # Create an act with title and summary
            act = act_manager.create_act(
                game_id=test_game.id,
                title="Context Test Act",
                summary="Created with session context",
            )

            # Verify the act was created correctly
            assert act.id is not None
            assert act.game_id == test_game.id
            assert act.title == "Context Test Act"
            assert act.summary == "Created with session context"
            assert act.sequence == 1
            assert act.is_active is True

            # Complete the first act before creating a new one
            act_manager.complete_act(act_id=act.id)

            # Create another act to test deactivation
            second_act = act_manager.create_act(
                game_id=test_game.id,
                title="Second Context Act",
            )

            # Refresh first act to verify it was deactivated
            session.refresh(act)
            assert act.is_active is False
            assert second_act.is_active is True

    def test_create_act_invalid_game(self, db_session, act_manager):
        """Test creating an act with an invalid game ID."""
        with pytest.raises(GameError):
            act_manager.create_act(
                game_id="invalid-id",
                title="Test Act",
            )

    def test_list_acts(
        self, db_session, test_game, test_act, create_test_act, act_manager
    ):
        """Test listing acts."""
        # Create a second act
        second_act = create_test_act(
            game_id=test_game.id,
            title="Second Act",
            sequence=2,
            is_active=False,
        )

        # List acts with explicit game_id
        acts = act_manager.list_acts(test_game.id)

        assert len(acts) == 2
        assert acts[0].id == test_act.id
        assert acts[1].id == second_act.id

        # Test listing acts with active game (requires mocking)
        from unittest.mock import patch

        with patch.object(
            act_manager.game_manager, "get_active_game", return_value=test_game
        ):
            acts = act_manager.list_acts()
            assert len(acts) == 2
            assert acts[0].id == test_act.id
            assert acts[1].id == second_act.id

        # Test listing acts with no active game
        with patch.object(
            act_manager.game_manager, "get_active_game", return_value=None
        ):
            with pytest.raises(GameError, match="No active game"):
                act_manager.list_acts()

    def test_get_act(self, db_session, test_act, act_manager):
        """Test getting an act by ID."""
        # Get existing act
        act = act_manager.get_act(test_act.id)

        assert act is not None
        assert act.id == test_act.id

        # Get non-existent act
        act = act_manager.get_act("invalid-id")

        assert act is None

    def test_get_active_act(self, db_session, test_game, test_act, act_manager):
        """Test getting the active act."""
        # Get active act with explicit game_id
        active_act = act_manager.get_active_act(test_game.id)

        assert active_act is not None
        assert active_act.id == test_act.id

        # Test getting active act with active game (requires mocking)
        from unittest.mock import patch

        with patch.object(
            act_manager.game_manager, "get_active_game", return_value=test_game
        ):
            active_act = act_manager.get_active_act()
            assert active_act is not None
            assert active_act.id == test_act.id

        # Deactivate all acts
        act_manager._deactivate_all_acts(db_session, test_game.id)
        db_session.commit()

        # Get active act when none is active
        active_act = act_manager.get_active_act(test_game.id)
        assert active_act is None

        # Test getting active act with no active game
        with patch.object(
            act_manager.game_manager, "get_active_game", return_value=None
        ):
            with pytest.raises(GameError, match="No active game"):
                act_manager.get_active_act()

    def test_edit_act(self, db_session, test_act, act_manager):
        """Test editing an act."""
        # Edit title only
        updated_act = act_manager.edit_act(
            act_id=test_act.id,
            title="Updated Title",
        )

        assert updated_act.title == "Updated Title"
        assert updated_act.summary == test_act.summary
        assert "updated-title" in updated_act.slug

        # Edit summary only
        updated_act = act_manager.edit_act(
            act_id=test_act.id,
            summary="Updated summary",
        )

        assert updated_act.title == "Updated Title"
        assert updated_act.summary == "Updated summary"

        # Edit both title and summary
        updated_act = act_manager.edit_act(
            act_id=test_act.id,
            title="Final Title",
            summary="Final summary",
        )

        assert updated_act.title == "Final Title"
        assert updated_act.summary == "Final summary"
        assert "final-title" in updated_act.slug

        # Edit non-existent act
        with pytest.raises(GameError):
            act_manager.edit_act(
                act_id="invalid-id",
                title="Invalid",
            )

    def test_edit_act_no_fields(self, db_session, test_act, act_manager):
        """Test editing an act without providing any fields."""
        with pytest.raises(ValueError, match="At least one of title or summary"):
            act_manager.edit_act(act_id=test_act.id)

    def test_complete_act(self, db_session, test_act, act_manager):
        """Test completing an act."""
        # Complete act
        completed_act = act_manager.complete_act(
            act_id=test_act.id,
            title="Completed Title",
            summary="Completed summary",
        )

        assert completed_act.title == "Completed Title"
        assert completed_act.summary == "Completed summary"
        assert completed_act.is_active is False
        assert "completed-title" in completed_act.slug

        # Complete non-existent act
        with pytest.raises(GameError):
            act_manager.complete_act(
                act_id="invalid-id",
            )

    def test_set_active(
        self, db_session, test_game, test_act, create_test_act, act_manager
    ):
        """Test setting an act as active."""
        # First, complete the existing active act
        act_manager.complete_act(act_id=test_act.id)

        # Create a second act
        second_act = create_test_act(
            game_id=test_game.id,
            title="Second Act",
            sequence=2,
            is_active=True,
        )

        # Refresh first act to see if it was deactivated
        db_session.refresh(test_act)
        assert test_act.is_active is False
        assert second_act.is_active is True

        # Set first act as active
        activated_act = act_manager.set_active(test_act.id)

        assert activated_act.id == test_act.id
        assert activated_act.is_active is True

        # Verify second act is inactive
        db_session.refresh(second_act)
        assert second_act.is_active is False

        # Set non-existent act as active
        with pytest.raises(GameError):
            act_manager.set_active("invalid-id")

        # Create another game and act
        from sologm.models.game import Game

        other_game = Game.create(name="Other Game", description="Another test game")
        db_session.add(other_game)
        db_session.flush()

        other_act = create_test_act(
            game_id=other_game.id,
            title="Other Act",
            sequence=1,
        )

        # Set act from different game as active (should work now since we don't validate game_id)
        other_activated_act = act_manager.set_active(other_act.id)
        assert other_activated_act.id == other_act.id
        assert other_activated_act.is_active is True

    def test_set_active_with_context(
        self, session_context, test_game, test_act, create_test_act
    ):
        """Test setting an act as active using session context."""
        with session_context as session:
            # Create act manager with session
            act_manager = ActManager(session=session)

            # First, complete the existing active act
            act_manager.complete_act(act_id=test_act.id)

            # Create a second act
            second_act = create_test_act(
                game_id=test_game.id,
                title="Second Context Act",
                sequence=2,
                is_active=True,
            )

            # Refresh first act to see if it was deactivated
            session.refresh(test_act)
            assert test_act.is_active is False
            assert second_act.is_active is True

            # Create act manager with session
            act_manager = ActManager(session=session)

            # Set first act as active
            activated_act = act_manager.set_active(test_act.id)

            assert activated_act.id == test_act.id
            assert activated_act.is_active is True

            # Verify second act is inactive
            session.refresh(second_act)
            assert second_act.is_active is False

    def test_validate_active_act(self, db_session, test_game, test_act, act_manager):
        """Test validating active act."""
        # Valid context with explicit game_id
        act = act_manager.validate_active_act(test_game.id)
        assert act.id == test_act.id

        # Test validating with active game (requires mocking)
        from unittest.mock import patch

        with patch.object(
            act_manager.game_manager, "get_active_game", return_value=test_game
        ):
            act = act_manager.validate_active_act()
            assert act.id == test_act.id

        # Deactivate all acts
        act_manager._deactivate_all_acts(db_session, test_game.id)
        db_session.commit()

        # Invalid context - no active act
        with pytest.raises(GameError, match="No active act"):
            act_manager.validate_active_act(test_game.id)

        # Test validating with no active game
        with patch.object(
            act_manager.game_manager, "get_active_game", return_value=None
        ):
            with pytest.raises(GameError, match="No active game"):
                act_manager.validate_active_act()

    def test_prepare_act_data_for_summary(
        self,
        db_session,
        test_game,
        test_act,
        test_scene,
        create_test_event,
        act_manager,
    ):
        """Test preparing act data for summary."""
        # Create some events for the scene
        event1 = create_test_event(scene_id=test_scene.id, description="First event")
        event2 = create_test_event(scene_id=test_scene.id, description="Second event")

        # Prepare data
        act_data = act_manager.prepare_act_data_for_summary(
            test_act.id, "Additional context"
        )

        # Verify structure
        assert act_data["game"]["name"] == test_game.name
        assert act_data["game"]["description"] == test_game.description
        assert act_data["act"]["sequence"] == test_act.sequence
        assert act_data["act"]["title"] == test_act.title
        assert act_data["act"]["summary"] == test_act.summary
        assert act_data["additional_context"] == "Additional context"

        # Verify scenes
        assert len(act_data["scenes"]) == 1
        scene_data = act_data["scenes"][0]
        assert scene_data["sequence"] == test_scene.sequence
        assert scene_data["title"] == test_scene.title
        assert scene_data["description"] == test_scene.description

        # Verify events
        assert len(scene_data["events"]) == 2
        event_descriptions = [e["description"] for e in scene_data["events"]]
        assert "First event" in event_descriptions
        assert "Second event" in event_descriptions

    def test_create_act_no_active_game(self, db_session, act_manager, monkeypatch):
        """Test creating an act without game_id when no game is active."""
        # Mock get_active_game to return None
        monkeypatch.setattr(act_manager.game_manager, "get_active_game", lambda: None)

        with pytest.raises(GameError, match="No active game"):
            act_manager.create_act(title="Test Act")

    def test_create_act_already_active(
        self, db_session, test_game, test_act, act_manager
    ):
        """Test creating an active act when another is already active."""
        # test_act is already active by default fixture setup
        with pytest.raises(GameError, match="Cannot create a new act"):
            act_manager.create_act(game_id=test_game.id, title="Another Active Act")

    def test_generate_and_update_act_summary(
        self, db_session, test_act, act_manager, monkeypatch
    ):
        """Test generating and updating act summary."""
        # Mock the generate_act_summary method
        mock_summary = {"title": "Generated Title", "summary": "Generated summary"}
        monkeypatch.setattr(
            act_manager, "generate_act_summary", lambda *args, **kwargs: mock_summary
        )

        # Test the method
        result = act_manager.generate_and_update_act_summary(
            test_act.id, "Additional context"
        )

        # Verify results
        assert result["title"] == "Generated Title"
        assert result["summary"] == "Generated summary"
        assert result["act"].id == test_act.id

        # Verify act was updated
        db_session.refresh(test_act)
        assert test_act.title == "Generated Title"
        assert test_act.summary == "Generated summary"

    def test_validate_can_create_act(
        self, db_session, test_game, test_act, act_manager
    ):
        """Test validating if a new act can be created."""
        # Should raise error when there's an active act
        with pytest.raises(GameError, match="Cannot create a new act"):
            act_manager.validate_can_create_act(test_game.id)

        # Deactivate the act
        test_act.is_active = False
        db_session.commit()

        # Should not raise error when there's no active act
        act_manager.validate_can_create_act(test_game.id)

    def test_generate_act_summary(self, db_session, test_act, act_manager, monkeypatch):
        """Test generating act summary."""
        # Mock the AnthropicClient and ActPrompts to avoid actual API calls
        from unittest.mock import MagicMock

        mock_client = MagicMock()
        mock_client.send_message.return_value = (
            "TITLE: Test Title\n\nSUMMARY:\nTest summary paragraph."
        )

        mock_prepare_data = MagicMock()
        mock_prepare_data.return_value = {
            "game": {"name": "Test Game", "description": "Test Description"},
            "act": {"sequence": 1, "title": "Test Act", "summary": "Test Summary"},
            "scenes": [],
            "additional_context": "Additional context",
        }

        # Apply mocks
        monkeypatch.setattr(
            act_manager, "prepare_act_data_for_summary", mock_prepare_data
        )
        monkeypatch.setattr(
            "sologm.integrations.anthropic.AnthropicClient", lambda: mock_client
        )

        # Test the method
        result = act_manager.generate_act_summary(test_act.id, "Additional context")

        # Verify results
        assert result["title"] == "Test Title"
        assert result["summary"] == "Test summary paragraph."

        # Verify mocks were called correctly
        mock_prepare_data.assert_called_once_with(test_act.id, "Additional context")
        mock_client.send_message.assert_called_once()

    def test_generate_act_summary_api_error(
        self, db_session, test_act, act_manager, monkeypatch
    ):
        """Test handling of API errors during summary generation."""
        # Mock the AnthropicClient to raise an error
        from unittest.mock import MagicMock

        mock_client = MagicMock()
        mock_client.send_message.side_effect = Exception("API connection failed")

        mock_prepare_data = MagicMock()
        mock_prepare_data.return_value = {
            "game": {"name": "Test Game", "description": "Test Description"},
            "act": {"sequence": 1, "title": "Test Act", "summary": "Test Summary"},
            "scenes": [],
            "additional_context": None,
        }

        # Apply mocks
        monkeypatch.setattr(
            act_manager, "prepare_act_data_for_summary", mock_prepare_data
        )
        monkeypatch.setattr(
            "sologm.integrations.anthropic.AnthropicClient", lambda: mock_client
        )

        # Test the method and assert APIError is raised
        from sologm.utils.errors import APIError

        with pytest.raises(APIError, match="Failed to generate act summary"):
            act_manager.generate_act_summary(test_act.id)

    def test_generate_act_summary_with_feedback(
        self, db_session, test_act, act_manager, monkeypatch
    ):
        """Test generating act summary with feedback on previous generation."""
        # Mock the generate_act_summary method
        mock_generate = MagicMock()
        mock_generate.return_value = {
            "title": "New Test Title",
            "summary": "New test summary paragraph.",
        }

        # Mock prepare_regeneration_context
        mock_prepare_context = MagicMock()
        mock_prepare_context.return_value = "Formatted regeneration context"

        # Apply mocks
        monkeypatch.setattr(act_manager, "generate_act_summary", mock_generate)
        monkeypatch.setattr(
            act_manager, "prepare_regeneration_context", mock_prepare_context
        )

        # Test with previous generation
        previous_gen = {"title": "Old Title", "summary": "Old summary"}

        result = act_manager.generate_act_summary_with_feedback(
            test_act.id, "User feedback", previous_gen
        )

        # Verify results
        assert result["title"] == "New Test Title"
        assert result["summary"] == "New test summary paragraph."

        # Verify mocks were called correctly
        mock_prepare_context.assert_called_once_with(previous_gen, "User feedback")
        mock_generate.assert_called_once_with(
            test_act.id, "Formatted regeneration context"
        )

        # Test without previous generation
        mock_generate.reset_mock()
        mock_prepare_context.reset_mock()

        result = act_manager.generate_act_summary_with_feedback(
            test_act.id, context="Just context"
        )

        # Verify results
        assert result["title"] == "New Test Title"
        assert result["summary"] == "New test summary paragraph."

        # Verify mocks were called correctly
        mock_prepare_context.assert_not_called()
        mock_generate.assert_called_once_with(test_act.id, "Just context")

    def test_prepare_regeneration_context(self, db_session, act_manager):
        """Test preparing regeneration context."""
        previous_gen = {"title": "Old Title", "summary": "Old summary paragraph."}

        # Test with just feedback
        context = act_manager.prepare_regeneration_context(
            previous_gen, "Make it more dramatic"
        )

        # Verify context structure
        assert "PREVIOUS GENERATION:" in context
        assert "Old Title" in context
        assert "Old summary paragraph." in context
        assert "USER FEEDBACK:" in context
        assert "Make it more dramatic" in context
        assert "INSTRUCTIONS:" in context

    def test_complete_act_with_ai(self, db_session, test_act, act_manager, monkeypatch):
        """Test completing an act with AI-generated content."""
        # Mock the complete_act method
        mock_complete = MagicMock()
        mock_complete.return_value = test_act

        # Apply mock
        monkeypatch.setattr(act_manager, "complete_act", mock_complete)

        # Test the method
        result = act_manager.complete_act_with_ai(test_act.id, "AI Title", "AI Summary")

        # Verify result
        assert result is test_act

        # Verify mock was called correctly
        mock_complete.assert_called_once_with(
            act_id=test_act.id, title="AI Title", summary="AI Summary"
        )
