"""Tests for event management functionality."""

import logging

import pytest

from sologm.models.event import Event
from sologm.models.game import Game
from sologm.utils.errors import EventError

logger = logging.getLogger(__name__)


class TestEventManager:
    """Tests for the EventManager class."""

    def test_add_event(self, event_manager, test_scene, db_session):
        """Test adding an event."""
        event = event_manager.add_event(
            description="Test event",
            scene_id=test_scene.id,
            source="manual",
        )

        assert event.scene_id == test_scene.id
        assert event.description == "Test event"
        assert event.source.name == "manual"

        # Verify event was saved to database
        db_event = db_session.query(Event).filter(Event.id == event.id).first()
        assert db_event is not None
        assert db_event.description == "Test event"

    def test_add_event_with_active_scene(self, event_manager, test_scene):
        """Test adding an event using the active scene."""
        event = event_manager.add_event(description="Test event with active scene")

        assert event.scene_id == test_scene.id
        assert event.description == "Test event with active scene"

    def test_add_event_nonexistent_scene(self, event_manager):
        """Test adding an event to a nonexistent scene."""
        with pytest.raises(EventError) as exc:
            event_manager.add_event(
                description="Test event",
                scene_id="nonexistent-scene",
            )
        assert "Scene nonexistent-scene not found" in str(exc.value)

    def test_list_events_empty(self, event_manager, test_scene):
        """Test listing events when none exist."""
        events = event_manager.list_events(scene_id=test_scene.id)
        assert len(events) == 0

    def test_list_events_with_active_scene(
        self, event_manager, test_scene, create_test_event
    ):
        """Test listing events using the active scene."""
        # Add some events
        create_test_event(test_scene.id, "First event")
        create_test_event(test_scene.id, "Second event")

        events = event_manager.list_events()
        assert len(events) == 2
        # Events should be in reverse chronological order (newest first)
        assert events[0].description == "Second event"
        assert events[1].description == "First event"

    def test_list_events(self, event_manager, test_scene, create_test_event):
        """Test listing multiple events."""
        # Add some events
        create_test_event(test_scene.id, "First event")
        create_test_event(test_scene.id, "Second event")

        events = event_manager.list_events(scene_id=test_scene.id)
        assert len(events) == 2
        # Events should be in reverse chronological order (newest first)
        assert events[0].description == "Second event"
        assert events[1].description == "First event"

    def test_list_events_with_limit(self, event_manager, test_scene, create_test_event):
        """Test listing events with a limit."""
        # Add some events
        create_test_event(test_scene.id, "First event")
        create_test_event(test_scene.id, "Second event")
        create_test_event(test_scene.id, "Third event")

        events = event_manager.list_events(scene_id=test_scene.id, limit=2)
        assert len(events) == 2
        assert events[0].description == "Third event"
        assert events[1].description == "Second event"

    def test_list_events_nonexistent_scene(self, event_manager):
        """Test listing events for a nonexistent scene."""
        with pytest.raises(EventError) as exc:
            event_manager.list_events(scene_id="nonexistent-scene")
        assert "Scene nonexistent-scene not found" in str(exc.value)

    def test_get_active_scene_id(self, event_manager, test_scene):
        """Test getting active scene ID."""
        scene_id = event_manager.get_active_scene_id()
        assert scene_id == test_scene.id

    def test_get_active_scene_id_no_game(self, event_manager, db_session):
        """Test getting active scene ID with no active game."""
        # Deactivate all games
        db_session.query(Game).update({Game.is_active: False})
        db_session.commit()

        with pytest.raises(EventError) as exc:
            event_manager.get_active_scene_id()
        assert "No active game found" in str(exc.value)

    def test_add_event_from_interpretation(
        self,
        event_manager,
        test_scene,
        test_interpretations,
        db_session,
    ):
        """Test adding an event from an interpretation."""
        interpretation = test_interpretations[0]

        event = event_manager.add_event(
            scene_id=test_scene.id,
            description="Event from interpretation",
            source="oracle",
            interpretation_id=interpretation.id,
        )

        assert event.interpretation_id == interpretation.id

        # Verify relationship works
        db_session.refresh(event)
        assert event.interpretation is not None
        assert event.interpretation.id == interpretation.id

    def test_get_event(self, event_manager, test_scene, create_test_event):
        """Test getting an event by ID."""
        # Create a test event
        logger.debug(f"Creating test event with scene_id={test_scene.id}")
        event = create_test_event(test_scene.id, "Test event to retrieve")
        logger.debug(
            f"Created event with id={event.id}, description={event.description}"
        )

        # Get the event
        retrieved_event = event_manager.get_event(event.id)
        logger.debug(f"Retrieved event: {retrieved_event}")
        if retrieved_event:
            logger.debug(
                f"Retrieved event id={retrieved_event.id}, "
                f"description={retrieved_event.description}"
            )

        # Verify the event was retrieved correctly
        assert retrieved_event is not None
        assert retrieved_event.id == event.id
        assert retrieved_event.description == "Test event to retrieve"

    def test_get_nonexistent_event(self, event_manager):
        """Test getting a nonexistent event."""
        # Try to get a nonexistent event
        event = event_manager.get_event("nonexistent-event-id")

        # Verify no event was found
        assert event is None

    def test_update_event(self, event_manager, test_scene, create_test_event):
        """Test updating an event's description."""
        # Create a test event
        logger.debug(f"Creating test event with scene_id={test_scene.id}")
        event = create_test_event(test_scene.id, "Original description")
        logger.debug(
            f"Created event with id={event.id}, description={event.description}"
        )
        logger.debug(f"Event source: {event.source_id}")
        if hasattr(event, "source") and event.source:
            logger.debug(f"Event source name: {event.source.name}")

        # Update the event
        updated_event = event_manager.update_event(event.id, "Updated description")
        logger.debug(f"Updated event: {updated_event}")
        logger.debug(f"Updated event description: {updated_event.description}")
        logger.debug(f"Updated event source_id: {updated_event.source_id}")
        if hasattr(updated_event, "source") and updated_event.source:
            logger.debug(f"Updated event source name: {updated_event.source.name}")

        # Verify the event was updated correctly
        assert updated_event.id == event.id
        assert updated_event.description == "Updated description"
        assert updated_event.source.name == "manual"  # Source should remain unchanged

        # Verify the event was updated in the database
        retrieved_event = event_manager.get_event(event.id)
        assert retrieved_event.description == "Updated description"

    def test_update_event_with_source(
        self, event_manager, test_scene, create_test_event
    ):
        """Test updating an event's description and source."""
        # Create a test event
        logger.debug(f"Creating test event with scene_id={test_scene.id}")
        event = create_test_event(test_scene.id, "Original description")
        logger.debug(
            f"Created event with id={event.id}, description={event.description}"
        )
        logger.debug(f"Event source_id: {event.source_id}")
        if hasattr(event, "source") and event.source:
            logger.debug(f"Event source name: {event.source.name}")

        # Check source name
        assert event.source.name == "manual"  # Default source

        # Update the event with a new source
        updated_event = event_manager.update_event(
            event.id, "Updated description", "oracle"
        )
        logger.debug(f"Updated event: {updated_event}")
        logger.debug(f"Updated event description: {updated_event.description}")
        logger.debug(f"Updated event source_id: {updated_event.source_id}")
        if hasattr(updated_event, "source") and updated_event.source:
            logger.debug(f"Updated event source name: {updated_event.source.name}")

        # Verify the event was updated correctly
        assert updated_event.id == event.id
        assert updated_event.description == "Updated description"
        assert updated_event.source.name == "oracle"  # Source should be updated

        # Verify the event was updated in the database
        retrieved_event = event_manager.get_event(event.id)
        assert retrieved_event.description == "Updated description"
        assert retrieved_event.source.name == "oracle"

    def test_update_nonexistent_event(self, event_manager):
        """Test updating a nonexistent event."""
        # Try to update a nonexistent event
        with pytest.raises(EventError) as exc:
            event_manager.update_event("nonexistent-event-id", "Updated description")

        # Verify the correct error was raised
        assert "Event with ID 'nonexistent-event-id' not found" in str(exc.value)

    def test_get_event_sources(self, event_manager):
        """Test getting all event sources."""
        # Get all event sources
        sources = event_manager.get_event_sources()

        # Verify we have the expected default sources
        assert len(sources) == 3
        source_names = [s.name for s in sources]
        assert "manual" in source_names
        assert "oracle" in source_names
        assert "dice" in source_names
