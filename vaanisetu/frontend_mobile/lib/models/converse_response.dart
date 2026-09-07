class ClarifyingQuestion {
  final String text;
  final List<String>? options;

  ClarifyingQuestion({required this.text, this.options});

  factory ClarifyingQuestion.fromJson(Map<String, dynamic> json) {
    return ClarifyingQuestion(
      text: json['text'],
      options: json['options'] != null ? List<String>.from(json['options']) : null,
    );
  }
}

class ResultDetail {
  final String scheme;
  final double confidence;
  final List<String> missingInfo;
  final List<String> reasoningTrace;

  ResultDetail({
    required this.scheme,
    required this.confidence,
    required this.missingInfo,
    required this.reasoningTrace,
  });

  factory ResultDetail.fromJson(Map<String, dynamic> json) {
    return ResultDetail(
      scheme: json['scheme'],
      confidence: (json['confidence'] as num).toDouble(),
      missingInfo: List<String>.from(json['missing_info']),
      reasoningTrace: List<String>.from(json['reasoning_trace']),
    );
  }
}

class ConverseResponse {
  final String mode; // "clarify" | "result"
  final ClarifyingQuestion? clarifyingQuestion;
  final ResultDetail? result;

  ConverseResponse({
    required this.mode,
    this.clarifyingQuestion,
    this.result,
  });

  factory ConverseResponse.fromJson(Map<String, dynamic> json) {
    return ConverseResponse(
      mode: json['mode'],
      clarifyingQuestion: json['clarifying_question'] != null
          ? ClarifyingQuestion.fromJson(json['clarifying_question'])
          : null,
      result: json['result'] != null
          ? ResultDetail.fromJson(json['result'])
          : null,
    );
  }
}

class AsrResponse {
  final String transcript;
  final String detectedLang;

  AsrResponse({required this.transcript, required this.detectedLang});

  factory AsrResponse.fromJson(Map<String, dynamic> json) {
    return AsrResponse(
      transcript: json['transcript'],
      detectedLang: json['detected_lang'],
    );
  }
}

class HealthStatus {
  final String status;
  final bool redisOk;
  final bool rfModelLoaded;
  final bool embeddingIndexLoaded;

  HealthStatus({
    required this.status,
    required this.redisOk,
    required this.rfModelLoaded,
    required this.embeddingIndexLoaded,
  });

  factory HealthStatus.fromJson(Map<String, dynamic> json) {
    return HealthStatus(
      status: json['status'],
      redisOk: json['redis_ok'],
      rfModelLoaded: json['rf_model_loaded'],
      embeddingIndexLoaded: json['embedding_index_loaded'],
    );
  }
}
