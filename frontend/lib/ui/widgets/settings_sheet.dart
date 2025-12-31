import 'package:flutter/material.dart';

class SettingsSheet extends StatefulWidget {
  final String initialPythonPath;
  final String initialCliPath;
  final void Function(String pythonPath, String cliPath) onSave;

  const SettingsSheet({
    super.key,
    required this.initialPythonPath,
    required this.initialCliPath,
    required this.onSave,
  });

  @override
  State<SettingsSheet> createState() => _SettingsSheetState();
}

class _SettingsSheetState extends State<SettingsSheet> {
  late final TextEditingController pythonController;
  late final TextEditingController cliController;

  @override
  void initState() {
    super.initState();
    pythonController = TextEditingController(text: widget.initialPythonPath);
    cliController = TextEditingController(text: widget.initialCliPath);
  }

  @override
  void dispose() {
    pythonController.dispose();
    cliController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    final scheme = Theme.of(context).colorScheme;

    return Padding(
      padding: EdgeInsets.only(bottom: mq.viewInsets.bottom),
      child: Container(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 16),
        decoration: const BoxDecoration(
          color: Color(0xFF0B0B10),
          borderRadius: BorderRadius.vertical(top: Radius.circular(18)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 48,
              height: 5,
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.18),
                borderRadius: BorderRadius.circular(999),
              ),
            ),
            const SizedBox(height: 16),
            const Row(
              children: [
                Icon(Icons.tune, size: 18),
                SizedBox(width: 10),
                Text(
                  "Execution Settings",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ],
            ),
            const SizedBox(height: 14),

            TextField(
              controller: pythonController,
              decoration: InputDecoration(
                labelText: "Python executable",
                hintText: "python  (or python3, or full path)",
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: scheme.outline.withValues(alpha: 0.25)),
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: scheme.primary.withValues(alpha: 0.6)),
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),

            const SizedBox(height: 12),

            TextField(
              controller: cliController,
              decoration: InputDecoration(
                labelText: "Backend entrypoint (main.py)",
                // Correct hint for your repo structure
                hintText: r"..\backend\main.py",
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: scheme.outline.withValues(alpha: 0.25)),
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: scheme.primary.withValues(alpha: 0.6)),
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),

            const SizedBox(height: 10),
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                r'Windows example: ..\backend\main.py   |   macOS/Linux: ../backend/main.py',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.white.withValues(alpha: 0.55),
                ),
              ),
            ),

            const SizedBox(height: 16),

            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text("Cancel"),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: FilledButton(
                    onPressed: () {
                      widget.onSave(
                        pythonController.text,
                        cliController.text,
                      );
                      Navigator.pop(context);
                    },
                    child: const Text("Save"),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
