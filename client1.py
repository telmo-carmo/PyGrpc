
import grpc
import simple1_pb2
import simple1_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:50051') as channel:
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
        list_response = stub.ListTodos(simple1_pb2.ListTodosRequest())
        print("All Todos:", list_response.todos)

        # Delete the Todo
        delete_response = stub.DeleteTodo(simple1_pb2.DeleteTodoRequest(id=create_response.todo.id))
        print("Delete Success:", delete_response.success)

if __name__ == '__main__':
    main()
