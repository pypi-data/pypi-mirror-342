import os
import unittest
import asyncio
from vibe_client.models import QueryAgentInput, ObservationValueBox
from vibe_client.client import VibeClient

class TestVibeClientQueryAgent(unittest.TestCase):
    """Test suite for the Vibe client query_agent functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Get authentication token from environment variables
        self.auth_token = os.environ.get('VIBE_AUTH_TOKEN')
        if not self.auth_token:
            self.skipTest("VIBE_AUTH_TOKEN environment variable not set")

        # Get endpoint from environment or use default
        self.endpoint = os.environ.get(
            'VIBE_ENDPOINT', 
            'https://8e2oorybga.execute-api.us-east-1.amazonaws.com/dev'
        )
        
        # Configure test data
        self.test_observations = ObservationValueBox([
            [1, 1.2, 3.0],
            [1, 1.2, 3.0],
            [1, 1.2, 3.0],
            [1, 1.2, 3.0],
            [1, 1.2, 3.0]
        ])
        
        # Get group and experiment IDs from environment or use defaults
        self.experiment_id = os.environ.get(
            'VIBE_EXPERIMENT_ID', 
            '8aeb428e-2588-4502-8943-0e2e402e1758'
        )
        
    async def _setup_client(self, token=None):
        """Helper to set up client with asyncio context."""
        client = VibeClient(
            api_key=token or self.auth_token,
            endpoint=self.endpoint
        )
        return client
        
    async def _test_query_agent(self, client):
        """Async test implementation."""
        query_input = QueryAgentInput(
            experiment_id=self.experiment_id,
            observations=self.test_observations
        )
        
        response = await client.query_agent(input=query_input)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.actions)
        return response

    def test_query_agent(self):
        """Test that query_agent returns the expected response."""
        async def run_test():
            client = await self._setup_client()
            response = await self._test_query_agent(client)
            print(f"Query response: {response}")
            print(f"Actions: {response.actions}")
            return response
            
        response = asyncio.run(run_test())
        # Additional assertions can be added here

    def test_query_agent_with_invalid_token(self):
        """Test that query_agent fails with an invalid token."""
        async def run_test():
            client = await self._setup_client(token="invalid_token")
            await self._test_query_agent(client)
            
        with self.assertRaises(Exception):
            asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()