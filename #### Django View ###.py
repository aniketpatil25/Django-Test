###views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
import json

# Utility function for raw SQL
def run_query(query, params=(), fetch=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetch:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    return None


# 1. Register Client
class ClientRegister(APIView):
    def post(self, request):
        data = request.data
        run_query("INSERT INTO client (name,email,phone) VALUES (%s,%s,%s)",
                  [data.get("name"), data.get("email"), data.get("phone")])
        return Response({"message": "Client registered successfully"})


# 2. Fetch Clients
class ClientList(APIView):
    def get(self, request):
        clients = run_query("SELECT * FROM client", fetch=True)
        return Response(clients)


# 3. Update/Delete Client
class ClientDetail(APIView):
    def put(self, request, client_id):
        data = request.data
        run_query("UPDATE client SET name=%s, email=%s, phone=%s WHERE id=%s",
                  [data.get("name"), data.get("email"), data.get("phone"), client_id])
        return Response({"message": "Client updated successfully"})

    def delete(self, request, client_id):
        run_query("DELETE FROM client WHERE id=%s", [client_id])
        return Response({"message": "Client deleted successfully"})


# 4. Add Project & Assign Users
class ProjectAdd(APIView):
    def post(self, request, client_id):
        data = request.data
        project_name, desc, user_ids = data.get("name"), data.get("description"), data.get("users", [])

        run_query("INSERT INTO project (client_id, name, description) VALUES (%s,%s,%s)", 
                  [client_id, project_name, desc])
        project_id = run_query("SELECT last_insert_rowid() as id", fetch=True)[0]["id"]

        for user_id in user_ids:
            run_query("INSERT INTO project_users (project_id, user_id) VALUES (%s,%s)", 
                      [project_id, user_id])

        return Response({"message": "Project created & users assigned"})


# 5. Retrieve Projects for Logged-in User
class MyProjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        projects = run_query("""
            SELECT p.id, p.name, p.description, c.name as client_name 
            FROM project p
            JOIN client c ON p.client_id = c.id
            JOIN project_users pu ON pu.project_id = p.id
            WHERE pu.user_id = %s
        """, [user_id], fetch=True)
        return Response(projects)

