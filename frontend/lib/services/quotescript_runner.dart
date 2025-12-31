import 'dart:io';
import 'package:path_provider/path_provider.dart';

class QuoteScriptRunResult {
  final int exitCode;
  final String stdoutText;
  final String stderrText;
  final Duration duration;

  const QuoteScriptRunResult({
    required this.exitCode,
    required this.stdoutText,
    required this.stderrText,
    required this.duration,
  });

  bool get ok => exitCode == 0;
}

class QuoteScriptRunner {
  /// Path to python executable: "python", "python3", or full path.
  String pythonPath;

  /// Path to your QuoteScript python entrypoint (backend/main.py).
  /// Can be relative or absolute.
  String cliScriptPath;

  QuoteScriptRunner({
    this.pythonPath = "python",
    String? cliScriptPath,
  }) : cliScriptPath = cliScriptPath ?? _defaultCliPath();

  static String _defaultCliPath() {
    // Your structure:
    // F:\QuoteScriptPROJECT\frontend\...
    // F:\QuoteScriptPROJECT\backend\main.py
    // So from frontend: ..\backend\main.py
    if (Platform.isWindows) return r"..\backend\main.py";
    return "../backend/main.py";
  }

  String _asText(dynamic v) {
    if (v == null) return "";
    if (v is String) return v;
    if (v is List<int>) return String.fromCharCodes(v);
    return v.toString();
  }

  /// Resolve cliScriptPath to an absolute path.
  /// If the configured path doesn't exist, walk upward until we find backend/main.py.
  String _resolveCliAbsPath() {
    final direct = File(cliScriptPath);
    if (direct.existsSync()) return direct.absolute.path;

    var dir = Directory.current;
    while (true) {
      final candidate = File(
        "${dir.path}${Platform.pathSeparator}backend${Platform.pathSeparator}main.py",
      );
      if (candidate.existsSync()) return candidate.absolute.path;

      final parent = dir.parent;
      if (parent.path == dir.path) break;
      dir = parent;
    }

    // If still not found, return the absolute version of what user provided.
    // (Python will fail with a clear error, but at least it's consistent.)
    return direct.absolute.path;
  }

  Future<QuoteScriptRunResult> run({
    required String scriptText,
  }) async {
    final sw = Stopwatch()..start();

    // Write the QS script to a temp file.
    final tmpDir = await getTemporaryDirectory();
    final qsFile = File("${tmpDir.path}${Platform.pathSeparator}example.qs");
    await qsFile.writeAsString(scriptText);

    final cliAbsPath = _resolveCliAbsPath();
    final cliFile = File(cliAbsPath);

    // Run: python <backend/main.py> <temp.qs>
    // workingDirectory set to backend/ so relative paths like data/db/... work.
    final res = await Process.run(
      pythonPath,
      [cliFile.path, qsFile.path],
      runInShell: true,
      workingDirectory: cliFile.parent.path,
    );

    sw.stop();

    return QuoteScriptRunResult(
      exitCode: res.exitCode,
      stdoutText: _asText(res.stdout),
      stderrText: _asText(res.stderr),
      duration: sw.elapsed,
    );
  }
}
