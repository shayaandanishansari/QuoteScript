import 'package:flutter/material.dart';
import '../services/quotescript_runner.dart';
import 'widgets/code_editor.dart';
import 'widgets/output_panel.dart';
import 'widgets/settings_sheet.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late final QuoteScriptRunner runner;
  late final TextEditingController _controller;

  QuoteScriptRunResult? lastResult;
  bool running = false;

  @override
  void initState() {
    super.initState();

    runner = QuoteScriptRunner(
      pythonPath: "python",
      cliScriptPath: r"..\backend\main.py",
    );

    _controller = TextEditingController(text: _defaultExample);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> runScript() async {
    setState(() {
      running = true;
      lastResult = null;
    });

    try {
      final res = await runner.run(scriptText: _controller.text);
      setState(() => lastResult = res);
    } catch (e) {
      setState(() {
        lastResult = QuoteScriptRunResult(
          exitCode: 1,
          stdoutText: "",
          stderrText: e.toString(),
          duration: Duration.zero,
        );
      });
    } finally {
      setState(() => running = false);
    }
  }

  void openSettings() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF0B0B10),
      builder: (_) => SettingsSheet(
        initialPythonPath: runner.pythonPath,
        initialCliPath: runner.cliScriptPath,
      onSave: (py, cli) {
        setState(() {
          final pyTrim = py.trim();
          final cliTrim = cli.trim();

          runner.pythonPath = pyTrim.isEmpty ? "python" : pyTrim;

          // CRITICAL:
          // If empty, keep existing value (do NOT force quotescript_cli.py)
          runner.cliScriptPath = cliTrim.isEmpty ? runner.cliScriptPath : cliTrim;
        });
      },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(18, 14, 18, 18),
          child: Column(
            children: [
              _TopBar(
                running: running,
                onRun: running ? null : runScript,
                onSettings: openSettings,
              ),
              const SizedBox(height: 14),
              Expanded(
                child: Row(
                  children: [
                    Expanded(
                      flex: 6,
                      child: _Panel(
                        title: "QuoteScript",
                        accent: scheme.primary,
                        child: CodeEditor(controller: _controller),
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      flex: 5,
                      child: _Panel(
                        title: "Output",
                        accent: scheme.tertiary,
                        child: OutputPanel(result: lastResult),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _TopBar extends StatelessWidget {
  final bool running;
  final VoidCallback? onRun;
  final VoidCallback onSettings;

  const _TopBar({
    required this.running,
    required this.onRun,
    required this.onSettings,
  });

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;

    return Row(
      children: [
        const Icon(Icons.code, size: 20),
        const SizedBox(width: 10),
        const Text(
          "QuoteScript Runner",
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
        const Spacer(),
        IconButton(
          onPressed: onSettings,
          icon: const Icon(Icons.settings),
          tooltip: "Settings",
        ),
        const SizedBox(width: 8),
        FilledButton.icon(
          onPressed: onRun,
          icon: const Icon(Icons.play_arrow),
          label: Text(running ? "Running..." : "Run"),
          style: FilledButton.styleFrom(
            backgroundColor: scheme.primary,
            foregroundColor: scheme.onPrimary,
          ),
        ),
      ],
    );
  }
}

class _Panel extends StatelessWidget {
  final String title;
  final Widget child;
  final Color? accent;

  const _Panel({
    required this.title,
    required this.child,
    this.accent,
  });

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final border = (accent ?? scheme.outline).withValues(alpha: 0.28);

    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF12121A),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: border),
      ),
      padding: const EdgeInsets.all(14),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 9,
                height: 9,
                decoration: BoxDecoration(
                  color: accent ?? scheme.primary,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 10),
              Text(
                title,
                style:
                    const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Expanded(child: child),
        ],
      ),
    );
  }
}

const String _defaultExample = r'''
QUOTE: "Freedom" exact

TOP: 5
RANDOM: 2
''';
