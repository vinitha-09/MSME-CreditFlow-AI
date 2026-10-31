"""Small schema-based A2A-style message helper for the prototype."""
def agent_message(sender: str, receiver: str, message_type: str, payload: dict) -> dict:
    if not all([sender, receiver, message_type]) or not isinstance(payload, dict):
        raise ValueError("A message needs sender, receiver, type and dictionary payload.")
    return {"sender": sender, "receiver": receiver, "type": message_type, "payload": payload}
