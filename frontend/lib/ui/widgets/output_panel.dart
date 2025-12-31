import 'package:flutter/material.dart';
import '../../services/quotescript_runner.dart';

class OutputPanel extends StatefulWidget {
  final QuoteScriptRunResult? result;

  const OutputPanel({super.key, required this.result});

  @override
  State<OutputPanel> createState() => _OutputPanelState();
}

class _OutputPanelState extends State<OutputPanel>
    with SingleTickerProviderStateMixin {
  late final TabController _tabs;

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabs.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final r = widget.result;

    final stdoutText = r?.stdoutText.trimRight() ?? "";
    final stderrText = r?.stderrText.trimRight() ?? "";

    return Column(
      children: [
        Container(
          padding: const EdgeInsets.fromLTRB(12, 10, 12, 0),
          child: Row(
            children: [
              Expanded(
                child: TabBar(
                  controller: _tabs,
                  isScrollable: true,
                  indicatorColor: scheme.primary,
                  dividerColor: Colors.white10,
                  tabs: const [
                    Tab(text: "Stdout / IR + Results"),
                    Tab(text: "Errors (stderr)"),
                  ],
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: TabBarView(
            controller: _tabs,
            children: [
              _ConsoleBox(
                emptyHint: "No output yet.\nClick Run.",
                text: stdoutText,
              ),
              _ConsoleBox(
                emptyHint: "No errors.",
                text: stderrText,
                errorMode: true,
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _ConsoleBox extends StatelessWidget {
  final String text;
  final String emptyHint;
  final bool errorMode;

  const _ConsoleBox({
    required this.text,
    required this.emptyHint,
    this.errorMode = false,
  });

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final color = errorMode ? const Color(0xFFEF4444) : scheme.onSurface;

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.all(12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF0B0B10),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white10),
      ),
      child: SingleChildScrollView(
        child: text.isEmpty
            ? Text(
                emptyHint,
                style: TextStyle(
                  fontSize: 12,
                  color: scheme.onSurface.withOpacity(0.55),
                ),
              )
            : SelectableText(
                text,
                style: TextStyle(
                  fontFamily: "monospace",
                  fontSize: 12.3,
                  height: 1.45,
                  color: color,
                ),
              ),
      ),
    );
  }
}
