import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'ui/home_page.dart';

void main() {
  runApp(const QuoteScriptApp());
}

class QuoteScriptApp extends StatelessWidget {
  const QuoteScriptApp({super.key});

  @override
  Widget build(BuildContext context) {
    const seed = Color(0xFF7C3AED); // violet
    final scheme = ColorScheme.fromSeed(
      seedColor: seed,
      brightness: Brightness.dark,
    );

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'QuoteScript Studio',
      theme: ThemeData(
        colorScheme: scheme,
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFF0B0B10),
        textTheme: const TextTheme(
          bodyMedium: TextStyle(fontSize: 14),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFF12121A),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: scheme.outline.withOpacity(0.35)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: scheme.outline.withOpacity(0.2)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: scheme.primary.withOpacity(0.8), width: 1.2),
          ),
        ),
      ),
      home: kIsWeb
          ? const _WebUnsupportedPage()
          : const HomePage(),
    );
  }
}

class _WebUnsupportedPage extends StatelessWidget {
  const _WebUnsupportedPage();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          padding: const EdgeInsets.all(24),
          constraints: const BoxConstraints(maxWidth: 520),
          decoration: BoxDecoration(
            color: const Color(0xFF12121A),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white12),
          ),
          child: const Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.public_off, size: 44),
              SizedBox(height: 12),
              Text(
                'QuoteScript Studio (Web)',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
              ),
              SizedBox(height: 8),
              Text(
                'This UI uses local Python execution via dart:io.\n'
                'That is not supported on Flutter Web.\n\n'
                'Run this app as a desktop build for your assignment demo.',
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
