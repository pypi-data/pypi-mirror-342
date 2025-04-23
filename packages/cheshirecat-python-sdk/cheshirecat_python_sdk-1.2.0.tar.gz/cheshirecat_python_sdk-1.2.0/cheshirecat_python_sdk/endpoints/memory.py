from typing import Dict, Any

from cheshirecat_python_sdk.enums import Collection, Role
from cheshirecat_python_sdk.endpoints.base import AbstractEndpoint
from cheshirecat_python_sdk.models.api.memories import (
    CollectionsOutput,
    CollectionPointsDestroyOutput,
    ConversationHistoryOutput,
    ConversationHistoryDeleteOutput,
    MemoryRecallOutput,
    MemoryPointOutput,
    MemoryPointDeleteOutput,
    MemoryPointsDeleteByMetadataOutput,
    MemoryPointsOutput,
)
from cheshirecat_python_sdk.models.dtos import Why, MemoryPoint


class MemoryEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/memory"

    # Memory Collections API

    def get_memory_collections(self, agent_id: str | None = None) -> CollectionsOutput:
        """
        This endpoint returns the collections of memory points, either for the agent identified by the agentId parameter
        (for multi-agent installations) or for the default agent (for single-agent installations).
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :return: CollectionsOutput, a list of collections of memory points.
        """
        return self.get(
            self.format_url("/collections"),
            CollectionsOutput,
            agent_id,
        )

    def delete_all_memory_collection_points(self, agent_id: str | None = None) -> CollectionPointsDestroyOutput:
        """
        This endpoint deletes all memory points in all collections for the agent identified by the agentId parameter
        (for multi-agent installations) or for the default agent (for single-agent installations).
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :return: CollectionPointsDestroyOutput, a message indicating the number of memory points deleted.
        """
        return self.delete(
            self.format_url("/collections"),
            CollectionPointsDestroyOutput,
            agent_id,
        )

    def delete_all_single_memory_collection_points(
        self, collection: Collection, agent_id: str | None = None
    ) -> CollectionPointsDestroyOutput:
        """
        This method deletes all the points in a single collection of memory, either for the agent identified by the
        agentId parameter (for multi-agent installations) or for the default agent (for single-agent installations).
        :param collection: The collection to delete.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :return: CollectionPointsDestroyOutput, a message indicating the number of memory points deleted.
        """
        return self.delete(
            self.format_url(f"/collections/{collection}"),
            CollectionPointsDestroyOutput,
            agent_id,
        )

    # END Memory Collections API

    # Memory Conversation History API

    def get_conversation_history(
        self, agent_id: str | None = None, user_id: str | None = None
    ) -> ConversationHistoryOutput:
        """
        This endpoint returns the conversation history, either for the agent identified by the agent_id parameter
        (for multi-agent installations) or for the default agent (for single-agent installations). If the user_id
        parameter is provided, the conversation history is filtered by the user ID.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :param user_id: The user ID to filter the conversation history.
        :return: ConversationHistoryOutput, a list of conversation history entries.
        """
        return self.get(
            self.format_url("/conversation_history"),
            ConversationHistoryOutput,
            agent_id,
            user_id,
        )

    def delete_conversation_history(
        self, agent_id: str | None = None, user_id: str | None = None
    ) -> ConversationHistoryDeleteOutput:
        """
        This endpoint deletes the conversation history, either for the agent identified by the agent_id parameter
        (for multi-agent installations) or for the default agent (for single-agent installations). If the user_id
        parameter is provided, the conversation history is filtered by the user ID.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :param user_id: The user ID to filter the conversation history.
        :return: ConversationHistoryDeleteOutput, a message indicating the number of conversation history entries deleted.
        """
        return self.delete(
            self.format_url("/conversation_history"),
            ConversationHistoryDeleteOutput,
            agent_id,
            user_id,
        )

    def post_conversation_history(
        self,
        who: Role,
        text: str,
        image: str | bytes | None = None,
        why: Why | None = None,
        agent_id: str | None = None,
        user_id: str | None = None
    ) -> ConversationHistoryOutput:
        """
        This endpoint creates a new element in the conversation history, either for the agent identified by the agent_id
        parameter (for multi-agent installations) or for the default agent (for single-agent installations). If the
        user_id parameter is provided, the conversation history is added to the user ID.
        :param who: The role of the user in the conversation.
        :param text: The text of the conversation history entry.
        :param image: The image of the conversation history entry.
        :param why: The reason for the conversation history entry.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :param user_id: The user ID to filter the conversation history.
        :return: ConversationHistoryOutput, the conversation history entry created.
        """
        payload = {
            "who": who.value,
            "text": text,
        }
        if image:
            payload["image"] = image
        if why:
            payload["why"] = why.model_dump()

        return self.post_json(
            self.format_url("/conversation_history"),
            ConversationHistoryOutput,
            payload,
            agent_id,
            user_id,
        )

    # END Memory Conversation History API

    # Memory Points API

    def get_memory_recall(
        self,
        text: str,
        k: int | None = None,
        metadata: Dict[str, Any] | None = None,
        agent_id: str | None = None,
        user_id: str | None = None,
    ) -> MemoryRecallOutput:
        """
        This endpoint retrieves memory points based on the input text, either for the agent identified by the agent_id
        parameter (for multi-agent installations) or for the default agent (for single-agent installations). The text
        parameter is the input text for which the memory points are retrieved. The k parameter is the number of memory
        points to retrieve.
        If the user_id parameter is provided, the memory points are filtered by the user ID.
        :param text: The input text for which the memory points are retrieved.
        :param k: The number of memory points to retrieve.
        :param metadata: The metadata to filter the memory points.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :param user_id: The user ID to filter the memory points.
        :return: MemoryRecallOutput, a list of memory points retrieved.
        """
        query = {"text": text}
        if k:
            query["k"] = k
        if metadata:
            query["metadata"] = metadata

        return self.get(
            self.format_url("/recall"),
            MemoryRecallOutput,
            agent_id,
            user_id,
            query,
        )

    def post_memory_point(
        self,
        collection: Collection,
        memory_point: MemoryPoint,
        agent_id: str | None = None,
        user_id: str | None = None,
    ) -> MemoryPointOutput:
        """
        This method posts a memory point, either for the agent identified by the agent_id parameter (for multi-agent
        installations) or for the default agent (for single-agent installations).
        If the user_id parameter is provided, the memory point is associated with the user ID.
        :param collection: The collection to post the memory point.
        :param memory_point: The memory point to post.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :param user_id: The user ID to associate with the memory point.
        :return: MemoryPointOutput, the memory point posted.
        """
        if user_id and not memory_point.metadata.get("source"):
            metadata = memory_point.metadata
            metadata["source"] = user_id
            memory_point.metadata = metadata

        return self.post_json(
            self.format_url(f"/collections/{collection}/points"),
            MemoryPointOutput,
            memory_point.model_dump(),
            agent_id,
        )

    def put_memory_point(
        self,
        collection: Collection,
        memory_point: MemoryPoint,
        point_id: str,
        agent_id: str | None = None,
        user_id: str | None = None,
    ) -> MemoryPointOutput:
        """
        This method puts a memory point, either for the agent identified by the agent_id parameter (for multi-agent
        installations) or for the default agent (for single-agent installations).
        If the user_id parameter is provided, the memory point is associated with the user ID.
        :param collection: The collection to put the memory point.
        :param memory_point: The memory point to put.
        :param point_id: The ID of the memory point to put.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :param user_id: The user ID to associate with the memory point.
        :return: MemoryPointOutput, the memory point put.
        """
        if user_id and not memory_point.metadata.get("source"):
            metadata = memory_point.metadata
            metadata["source"] = user_id
            memory_point.metadata = metadata

        return self.put(
            self.format_url(f"/collections/{collection}/points/{point_id}"),
            MemoryPointOutput,
            memory_point.model_dump(),
            agent_id,
        )

    def delete_memory_point(
        self,
        collection: Collection,
        point_id: str,
        agent_id: str | None = None,
    ) -> MemoryPointDeleteOutput:
        """
        This endpoint deletes a memory point, either for the agent identified by the agent_id parameter (for multi-agent
        installations) or for the default agent (for single-agent installations).
        :param collection: The collection to delete the memory point.
        :param point_id: The ID of the memory point to delete.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :return: MemoryPointDeleteOutput, a message indicating the memory point deleted.
        """
        return self.delete(
            self.format_url(f"/collections/{collection}/points/{point_id}"),
            MemoryPointDeleteOutput,
            agent_id,
        )

    def delete_memory_points_by_metadata(
        self,
        collection: Collection,
        metadata: Dict[str, Any] | None = None,
        agent_id: str | None = None,
    ) -> MemoryPointsDeleteByMetadataOutput:
        """
        This endpoint deletes memory points based on the metadata, either for the agent identified by the agent_id
        parameter (for multi-agent installations) or for the default agent (for single-agent installations). The
        metadata parameter is a dictionary of key-value pairs that the memory points must match.
        :param collection: The collection to delete the memory points.
        :param metadata: The metadata to filter the memory points.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :return: MemoryPointsDeleteByMetadataOutput, a message indicating the number of memory points deleted.
        """
        return self.delete(
            self.format_url(f"/collections/{collection}/points"),
            MemoryPointsDeleteByMetadataOutput,
            agent_id,
            payload=metadata,
        )

    def get_memory_points(
        self,
        collection: Collection,
        limit: int | None = None,
        offset: int | None = None,
        agent_id: str | None = None,
    ) -> MemoryPointsOutput:
        """
        This endpoint retrieves memory points, either for the agent identified by the agent_id parameter (for
        multi-agent installations) or for the default agent (for single-agent installations). The limit parameter is the
        maximum number of memory points to retrieve. The offset parameter is the number of memory points to skip.
        :param collection: The collection to retrieve the memory points.
        :param limit: The maximum number of memory points to retrieve.
        :param offset: The number of memory points to skip.
        :param agent_id: The agent ID for multi-agent installations. If not provided, the default agent is used.
        :return: MemoryPointsOutput, a list of memory points retrieved.
        """
        query = {}
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset

        return self.get(
            self.format_url(f"/collections/{collection}/points"),
            MemoryPointsOutput,
            agent_id,
            query=query,
        )

    # END Memory Points API
