import argparse, random
import grpc
from datetime import datetime
import simple1_pb2
import simple1_pb2_grpc

def main():
    parser = argparse.ArgumentParser(description="gRPC TodoService Client")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=50051,
        nargs="?",
        help="The port on which the server listens.",
    )
    parser.add_argument(
        "--host",
        type=str, 
        default="localhost", 
        help="The server host to connect to.") 

    args = parser.parse_args()

    with grpc.insecure_channel(f'{args.host}:{args.port}') as channel:
        stub = simple1_pb2_grpc.TodoServiceStub(channel)

        # Create a Todo
        create_response = stub.CreateTodo(simple1_pb2.CreateTodoRequest(name="Buy milk", done=False))
        print("Created Todo:", create_response.todo)

        # Get the Todo
        get_response = stub.GetTodo(simple1_pb2.GetTodoRequest(id=create_response.todo.id))
        print("Fetched Todo:", get_response.todo)

        # Update the Todo
        update_response = stub.UpdateTodo(simple1_pb2.UpdateTodoRequest(id=create_response.todo.id, name="Buy milk and eggs", done=True))
        print("Updated Todo:", update_response.todo)

        # List all Todos
        list_response = stub.ListTodos(simple1_pb2.ListTodosRequest(),
            metadata=[
                ("metadata-1", datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] ),
                ('accesstoken', 'GRPC-Client-Token-{}'.format(random.randint(1000, 9999)))]
        )
        print("All Todos:", list_response.todos)

        # Delete the Todo
        delete_response = stub.DeleteTodo(simple1_pb2.DeleteTodoRequest(id=create_response.todo.id))
        print("Delete Success:", delete_response.success)

if __name__ == '__main__':
    main()
