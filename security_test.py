
import unittest

from rafeeq import (
    ALLOWED_EMAIL_DOMAINS,
    book_inspection,
    egress_guard,
    get_permit_status,
    send_email,
)


class SecurityTests(unittest.TestCase):

    def test_allowed_internal_domain(self):
        allowed, _ = egress_guard("review@madar.example")
        self.assertTrue(allowed)

    def test_blocks_external_domain(self):
        allowed, reason = egress_guard("attacker@external.example")
        self.assertFalse(allowed)
        self.assertIn("not allowlisted", reason)

    def test_blocks_malformed_recipient(self):
        allowed, _ = egress_guard("not-an-email")
        self.assertFalse(allowed)

    def test_email_requires_approval(self):
        result = send_email(
            "review@madar.example",
            "Test",
            "Testing only",
            approved=False,
        )
        self.assertTrue(result["approval_required"])
        self.assertFalse(result["success"])

    def test_external_email_is_blocked_even_if_approved(self):
        result = send_email(
            "attacker@external.example",
            "Test",
            "Testing only",
            approved=True,
        )
        self.assertTrue(result["blocked"])
        self.assertFalse(result["success"])

    def test_booking_requires_approval(self):
        result = book_inspection(
            "2026-11-02 09:00",
            approved=False,
        )
        self.assertTrue(result["approval_required"])
        self.assertFalse(result["success"])

    def test_booking_rejects_non_boolean_approval(self):
        result = book_inspection(
            "2026-11-02 09:00",
            approved="yes",
        )
        self.assertFalse(result["success"])
        self.assertTrue(result["approval_required"])

    def test_invalid_booking_slot_is_rejected(self):
        result = book_inspection(
            "2099-01-01 00:00",
            approved=True,
        )
        self.assertFalse(result["success"])

    def test_permit_details_are_limited(self):
        result = get_permit_status("P-1001")
        self.assertIn("status", result)
        self.assertNotIn("applicant_name", result)
        self.assertNotIn("phone_number", result)

    def test_allowlist_is_not_empty(self):
        self.assertTrue(ALLOWED_EMAIL_DOMAINS)

    
    def test_mcp_rejects_non_object_arguments(self):
        import mcp_server

        response = mcp_server.respond({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search_policies",
                "arguments": "unexpected",
            },
        })

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32600)
        self.assertEqual(
            response["error"]["message"],
            "Tool arguments must be an object",
        )

    
    def test_mcp_rejects_non_object_params(self):
        import mcp_server

        response = mcp_server.respond({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": "unexpected",
        })

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32600)
        self.assertEqual(
            response["error"]["message"],
            "Invalid request parameters",
        )

    
    def test_mcp_rejects_non_object_message(self):
        import mcp_server

        response = mcp_server.respond("unexpected")

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32600)
        self.assertEqual(
            response["error"]["message"],
            "Invalid request: message must be an object",
        )

    
    def test_mcp_rejects_non_string_query(self):
        import mcp_server

        response = mcp_server.respond({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "search_policies",
                "arguments": {"query": 123},
            },
        })

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32602)
        self.assertEqual(
            response["error"]["message"],
            "Query must be a string",
        )

    
    def test_mcp_rejects_unknown_tool(self):
        import mcp_server

        response = mcp_server.respond({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "delete_all_records",
                "arguments": {},
            },
        })

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)
        self.assertEqual(response["error"]["message"], "Unknown tool")

    
    def test_mcp_rejects_missing_tool_name(self):
        import mcp_server

        response = mcp_server.respond({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "arguments": {"query": "permit"},
            },
        })

        self.assertIn("error", response)
        self.assertEqual(response["error"]["code"], -32601)
        self.assertEqual(response["error"]["message"], "Unknown tool")






if __name__ == "__main__":
    unittest.main(verbosity=2)
