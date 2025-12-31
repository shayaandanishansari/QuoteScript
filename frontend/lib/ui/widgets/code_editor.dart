import 'package:flutter/material.dart';

class CodeEditor extends StatefulWidget {
  final TextEditingController controller;

  const CodeEditor({super.key, required this.controller});

  @override
  State<CodeEditor> createState() => _CodeEditorState();
}

class _CodeEditorState extends State<CodeEditor> {
  final ScrollController _codeScroll = ScrollController();
  final ScrollController _lineScroll = ScrollController();

  @override
  void initState() {
    super.initState();
    _codeScroll.addListener(_syncScroll);
  }

  @override
  void dispose() {
    _codeScroll.removeListener(_syncScroll);
    _codeScroll.dispose();
    _lineScroll.dispose();
    super.dispose();
  }

  void _syncScroll() {
    if (_lineScroll.hasClients) {
      _lineScroll.jumpTo(_codeScroll.offset);
    }
  }

  int get _lineCount {
    final text = widget.controller.text;
    if (text.isEmpty) return 1;
    return '\n'.allMatches(text).length + 1;
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;

    return Container(
      padding: const EdgeInsets.all(12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Line numbers
          SizedBox(
            width: 46,
            child: SingleChildScrollView(
              controller: _lineScroll,
              child: AnimatedBuilder(
                animation: widget.controller,
                builder: (context, _) {
                  final lines = _lineCount;
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: List.generate(lines, (i) {
                      return Padding(
                        padding: const EdgeInsets.only(right: 8, bottom: 2),
                        child: Text(
                          "${i + 1}",
                          style: TextStyle(
                            fontFamily: "monospace",
                            fontSize: 12.2,
                            color: scheme.onSurface.withOpacity(0.35),
                            height: 1.45,
                          ),
                        ),
                      );
                    }),
                  );
                },
              ),
            ),
          ),
          const SizedBox(width: 6),

          // Code area
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: const Color(0xFF0B0B10),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.white10),
              ),
              child: Scrollbar(
                controller: _codeScroll,
                thumbVisibility: true,
                child: SingleChildScrollView(
                  controller: _codeScroll,
                  padding: const EdgeInsets.fromLTRB(12, 10, 12, 12),
                  child: TextField(
                    controller: widget.controller,
                    maxLines: null,
                    style: const TextStyle(
                      fontFamily: "monospace",
                      fontSize: 12.8,
                      height: 1.45,
                    ),
                    decoration: const InputDecoration(
                      isDense: true,
                      border: InputBorder.none,
                      hintText:
                          'Write QuoteScript here...\n'
                          'Example:\n'
                          'QUOTE: "Freedom" exact\n'
                          'AUTHOR: "Epictetus" forgiving\n'
                          'TOP: 5\n'
                          'RANDOM 2',
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
