PYTHON ?= uv run python
PROTO_DIR := app/proto
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)

.PHONY: proto proto-clean proto-check

proto: proto-check
	$(PYTHON) -m grpc_tools.protoc -I . --python_out=. --pyi_out=. --grpc_python_out=. $(PROTO_FILES)

ifeq ($(strip $(PROTO_FILES)),)
proto-check:
	@echo No .proto files found in $(PROTO_DIR)
	@exit 1
else
proto-check:
	@$(PYTHON) -c "pass"
endif

proto-clean:
	$(PYTHON) -c "import glob, os; \
		root=r'$(PROTO_DIR)'; \
		[os.remove(p) for pat in ('*_pb2.py','*_pb2.pyi','*_pb2_grpc.py') for p in glob.glob(os.path.join(root, pat))]"
