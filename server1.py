'''

python -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/simple1.proto


'''

import grpc
from concurrent import futures
import time, logging, argparse
import simple1_pb2
import simple1_pb2_grpc

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s ; %(levelname)s ; %(message)s')

class TodoService(simple1_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        self.todos = {}
        self.next_id = 1
        self.add_todo("Buy coffee", False)
        self.add_todo("Walk the dog", True) 
        self.add_todo("Read a book", False)
        self.add_todo("Write code", True)

    def add_todo(self, name : str, done : bool) -> simple1_pb2.Todo:
        todo = simple1_pb2.Todo(
            id=self.next_id,
            name=name,
            done=done
        )
        self.todos[self.next_id] = todo
        self.next_id += 1
        return todo

    def CreateTodo(self, request, context):
        todo = simple1_pb2.Todo(
            id=self.next_id,
            name=request.name,
            done=request.done
        )
        self.todos[self.next_id] = todo
        self.next_id += 1
        logger.info(f"Created Todo with ID: {self.next_id - 1}")
        return simple1_pb2.CreateTodoResponse(todo=todo)

    def GetTodo(self, request, context):
        todo = self.todos.get(request.id)
        logger.info(f"Get Todo with ID {request.id}")
        if todo:
            return simple1_pb2.GetTodoResponse(todo=todo)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Todo not found')
        logger.warning(f"Todo with ID {request.id} not found")
        return simple1_pb2.GetTodoResponse()

    def UpdateTodo(self, request, context):
        todo = self.todos.get(request.id)
        logger.info(f"Update Todo with ID {request.id}")
        if todo:
            todo.name = request.name
            todo.done = request.done
            self.todos[request.id] = todo
            return simple1_pb2.UpdateTodoResponse(todo=todo)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Todo not found')
        return simple1_pb2.UpdateTodoResponse()

    def DeleteTodo(self, request, context):
        logger.info(f"Delete Todo with ID {request.id}")
        if request.id in self.todos:
            del self.todos[request.id]
            return simple1_pb2.DeleteTodoResponse(success=True)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Todo not found')
        logger.warning(f"Todo with ID {request.id} not found for deletion")
        return simple1_pb2.DeleteTodoResponse(success=False)

    def ListTodos(self, request, context):
        logger.info(f"List all Todos #%d" ,len(self.todos.values()))
        return simple1_pb2.ListTodosResponse(todos=list(self.todos.values()))

def serve():
    parser = argparse.ArgumentParser(description="gRPC TodoService Server")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=50051,
        nargs="?",
        help="The port on which the server will listen.",
    )
    args = parser.parse_args()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple1_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:{}'.format(args.port))
    server.start()
    logger.info('TodoService server started on port %s', args.port)
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
