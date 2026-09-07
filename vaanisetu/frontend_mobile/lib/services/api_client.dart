import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config/env.dart';
import '../models/converse_response.dart';

class ApiClient {
  final String baseUrl = Env.backendBaseUrl;

  Future<AsrResponse> transcribe(File audio, {String? langHint}) async {
    final uri = Uri.parse('$baseUrl/asr');
    var request = http.MultipartRequest('POST', uri);
    
    if (langHint != null) {
      request.fields['lang_hint'] = langHint;
    }
    
    request.files.add(await http.MultipartFile.fromPath('audio', audio.path));
    
    var streamedResponse = await request.send();
    var response = await http.Response.fromStream(streamedResponse);
    
    if (response.statusCode == 200) {
      return AsrResponse.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to transcribe audio: ${response.statusCode}');
    }
  }

  Future<ConverseResponse> converse(String sessionId, String transcript) async {
    final uri = Uri.parse('$baseUrl/converse');
    
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'session_id': sessionId,
        'transcript': transcript,
      }),
    );
    
    if (response.statusCode == 200) {
      return ConverseResponse.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to converse: ${response.statusCode}');
    }
  }

  Future<String> synthesize(String text, String lang) async {
    final uri = Uri.parse('$baseUrl/tts');
    
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'text': text,
        'lang': lang,
      }),
    );
    
    if (response.statusCode == 200) {
      final jsonResponse = json.decode(response.body);
      return jsonResponse['audio_url'];
    } else {
      throw Exception('Failed to synthesize text: ${response.statusCode}');
    }
  }

  Future<HealthStatus> checkHealth() async {
    // Health is at the root level, so we strip /api from the baseUrl for this request
    final healthBaseUrl = baseUrl.endsWith('/api') 
      ? baseUrl.substring(0, baseUrl.length - 4) 
      : baseUrl;
      
    final uri = Uri.parse('$healthBaseUrl/health');
    final response = await http.get(uri);
    
    if (response.statusCode == 200) {
      return HealthStatus.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to check health: ${response.statusCode}');
    }
  }
}
