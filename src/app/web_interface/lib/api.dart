class APICaller {
  static final APICaller _instance = APICaller._internal();
  factory APICaller() {
    return _instance;
  }
  APICaller._internal();

  static String baseUrl = "";
  static String endpoint = "$baseUrl/";

  addPackage({required String url}) {}

  deletePackages() {}

  updatePackages() {}

  factoryReset() {}
}
