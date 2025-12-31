import 'dart:io';
import 'package:path/path.dart' as p;
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
  /// Dev fallback only (when bundled exe isn't found)
  String pythonPath;

  /// Dev fallback only: path to backend/main.py
  String cliScriptPath;

  QuoteScriptRunner({
    this.pythonPath = "python",
    String? cliScriptPath,
  }) : cliScriptPath = cliScriptPath ?? _defaultCliPath();

  static String _defaultCliPath() {
    if (Platform.isWindows) return r"..\backend\main.py";
    return "../backend/main.py";
  }

  String _asText(dynamic v) {
    if (v == null) return "";
    if (v is String) return v;
    if (v is List<int>) return String.fromCharCodes(v);
    return v.toString();
  }

  Directory _appDir() {
    // Path to the running executable:
    // Windows: .../Release/YourApp.exe
    // Linux:   .../bundle/your_app
    // macOS:   .../YourApp.app/Contents/MacOS/YourApp
    return File(Platform.resolvedExecutable).parent;
  }

  List<File> _bundledBackendCandidates() {
    final dir = _appDir().path;
    final exeName = Platform.isWindows ? "quotescript_cli.exe" : "quotescript_cli";

    return [
      // What our GitHub Actions will bundle:
      File(p.join(dir, "quotescript_cli", exeName)),

      // Optional alternative layouts (safe to check):
      File(p.join(dir, exeName)),
      File(p.join(dir, "backend", exeName)),
    ];
  }

  File? _findBundledBackend() {
    for (final f in _bundledBackendCandidates()) {
      if (f.existsSync()) return f;
    }
    return null;
  }

  String _resolveDevScriptAbsPath() {
    final direct = File(cliScriptPath);
    if (direct.existsSync()) return direct.absolute.path;

    // Walk upward and try to find backend/main.py (useful if cwd differs)
    var dir = Directory.current;
    while (true) {
      final candidate = File(p.join(dir.path, "backend", "main.py"));
      if (candidate.existsSync()) return candidate.absolute.path;

      final parent = dir.parent;
      if (parent.path == dir.path) break;
      dir = parent;
    }

    return direct.absolute.path; // will fail with a clear python error if wrong
  }

  Future<QuoteScriptRunResult> run({required String scriptText}) async {
    final sw = Stopwatch()..start();

    // Write QS to a temp file
    final tmpDir = await getTemporaryDirectory();
    final qsFile = File(p.join(tmpDir.path, "example.qs"));
    await qsFile.writeAsString(scriptText);

    ProcessResult res;

    final bundled = _findBundledBackend();
    if (bundled != null) {
      // Production mode: run bundled native backend
      res = await Process.run(
        bundled.path,
        [qsFile.path],
        runInShell: true,
        workingDirectory: bundled.parent.path,
      );
    } else {
      // Dev mode fallback: python backend/main.py <file>
      final scriptAbs = _resolveDevScriptAbsPath();
      final scriptFile = File(scriptAbs);

      res = await Process.run(
        pythonPath,
        [scriptFile.path, qsFile.path],
        runInShell: true,
        workingDirectory: scriptFile.parent.path,
      );
    }

    sw.stop();

    return QuoteScriptRunResult(
      exitCode: res.exitCode,
      stdoutText: _asText(res.stdout),
      stderrText: _asText(res.stderr),
      duration: sw.elapsed,
    );
  }
}
