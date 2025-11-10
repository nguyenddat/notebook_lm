import json

def generate_stream(gen):
    try:
        chunk_count = 0
        final_resp = ""
        citations = []

        for chunk in gen:
            chunk_count += 1
            if isinstance(chunk, dict):
                final_resp = chunk.get("response", "")
                citations = chunk.get("citations", [])
                continue
            else:
                yield f"data: {json.dumps({'type': 'content', 'chunk_id': chunk_count, 'content': chunk, 'status': 'streaming'}, ensure_ascii=False)}\n\n"

        # yield cuối cùng
        yield f"data: {json.dumps({'type': 'end', 'chunk_id': chunk_count, 'content': final_resp, 'status': 'completed', 'citations': citations}, ensure_ascii=False)}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'type': 'end', 'chunk_id': 0, 'status': 'completed', 'content': 'error', 'citations': [], 'error': str(e)}, ensure_ascii=False)}\n\n"
    finally:
        yield "event: close\ndata: {}\n\n"

