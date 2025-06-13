Attribute VB_Name = "Recalculo"
Option Explicit

Sub ActualizarHallazgos()
    Dim py As String
    py = ThisWorkbook.Path & "\update_hallazgos.py"
    Shell "python """ & py & """", vbNormalFocus
End Sub
