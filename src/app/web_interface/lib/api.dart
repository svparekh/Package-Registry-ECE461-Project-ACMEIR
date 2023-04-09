class APICaller {
  static final APICaller _instance = APICaller._internal();
  factory APICaller() {
    return _instance;
  }
  APICaller._internal();

  static String baseUrl = "";
  static String endpoint = "$baseUrl/";

  addPackage({required String url}) {
    print("added $url");
    // Must check if package with same name and version already exists or not
  }

  deletePackages() {}

  updatePackages() {}

  factoryReset() {}
}
