import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'services/api_client.dart';
import 'models/converse_response.dart';

void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'VaaniSetu',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const HealthCheckScreen(),
    );
  }
}

class HealthCheckScreen extends StatefulWidget {
  const HealthCheckScreen({super.key});

  @override
  State<HealthCheckScreen> createState() => _HealthCheckScreenState();
}

class _HealthCheckScreenState extends State<HealthCheckScreen> {
  final ApiClient _apiClient = ApiClient();
  HealthStatus? _healthStatus;
  String? _error;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _checkHealth();
  }

  Future<void> _checkHealth() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final status = await _apiClient.checkHealth();
      setState(() {
        _healthStatus = status;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('VaaniSetu Checkpoint 1'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (_isLoading) const CircularProgressIndicator(),
              if (_error != null)
                Text(
                  'Error: $_error',
                  style: const TextStyle(color: Colors.red),
                ),
              if (_healthStatus != null) ...[
                const Icon(Icons.check_circle, color: Colors.green, size: 64),
                const SizedBox(height: 16),
                Text('Status: ${_healthStatus!.status}',
                    style: const TextStyle(fontSize: 20)),
                Text('Redis OK: ${_healthStatus!.redisOk}'),
                Text('RF Model Loaded: ${_healthStatus!.rfModelLoaded}'),
                Text('Embedding Index: ${_healthStatus!.embeddingIndexLoaded}'),
              ],
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: _checkHealth,
                child: const Text('Refresh Health Check'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
