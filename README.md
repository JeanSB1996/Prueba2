 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 5eba6dbff53e8bedf5ae64a1b028765db4069549..5ab3439510337b34160d1a066a1bcb14ea1112ac 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,5 @@
 # Prueba2
+
 Pre informe auditoria laboral
+
+Este repositorio contiene el pre informe de auditoria actualizado con los hallazgos y recomendaciones derivados del analisis de gratificacion 2024.
 
EOF
)
