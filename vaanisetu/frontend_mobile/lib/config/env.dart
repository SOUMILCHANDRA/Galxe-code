class Env {
  // Use http://10.0.2.2:8000/api for local Android emulator testing
  static const String backendBaseUrl = String.fromEnvironment(
    'BACKEND_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api',
  );
}
