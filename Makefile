PYTHON ?= uv run python
PROTO_DIR := app/proto
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)

.PHONY: proto proto-clean proto-check

proto: proto-check
	$(PYTHON) -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. $(PROTO_FILES)

proto-check:
	@test -n "$(PROTO_FILES)" || (echo "No .proto files found in $(PROTO_DIR)"; exit 1)

proto-clean:
	rm -f $(PROTO_DIR)/*_pb2.py $(PROTO_DIR)/*_pb2.pyi $(PROTO_DIR)/*_pb2_grpc.py
