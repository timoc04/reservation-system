import pyodbc

from .config import Config


def get_connection():
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={Config.DB_SERVER};"
        f"DATABASE={Config.DB_NAME};"
        f"UID={Config.DB_USERNAME};"
        f"PWD={Config.DB_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    return pyodbc.connect(connection_string)


def initialise_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects
            WHERE name='Reservations' AND xtype='U'
        )
        CREATE TABLE Reservations (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            GuestName NVARCHAR(255) NOT NULL,
            Accommodation NVARCHAR(255) NOT NULL,
            StartDate DATE NOT NULL,
            EndDate DATE NOT NULL,
            CreatedBy NVARCHAR(255) NOT NULL,
            CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
            Status NVARCHAR(50) NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def create_reservation(guest_name, accommodation, start_date, end_date, created_by):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Reservations
        (GuestName, Accommodation, StartDate, EndDate, CreatedBy, Status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, guest_name, accommodation, start_date, end_date, created_by, "Created")

    connection.commit()
    cursor.close()
    connection.close()


def get_all_reservations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            Id,
            GuestName,
            Accommodation,
            StartDate,
            EndDate,
            CreatedBy,
            CreatedAt,
            Status
        FROM Reservations
        ORDER BY CreatedAt DESC
    """)

    rows = cursor.fetchall()

    reservations = []
    for row in rows:
        reservations.append({
            "id": row.Id,
            "guest_name": row.GuestName,
            "accommodation": row.Accommodation,
            "start_date": row.StartDate,
            "end_date": row.EndDate,
            "created_by": row.CreatedBy,
            "created_at": row.CreatedAt,
            "status": row.Status
        })

    cursor.close()
    connection.close()

    return reservations