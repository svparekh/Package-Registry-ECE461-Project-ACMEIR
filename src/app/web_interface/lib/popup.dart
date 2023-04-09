import 'dart:async';

import 'package:fluent_ui/fluent_ui.dart';
import 'package:web_interface/api.dart';

Future<bool> showPackageDialog(BuildContext context,
    {required String type, List<Map<String, dynamic>>? packages}) async {
  // Type can be of types: 'Add', 'Update', or 'Delete'
  // Returns false if canceled and true if main action button pressed
  final bool? result = await showDialog<bool>(
    context: context,
    builder: (context) {
      // Vars and stream setup
      final TextEditingController controller = TextEditingController();
      StreamController<bool> isWorkingStream =
          StreamController<bool>.broadcast();
      isWorkingStream.add(false);
      // Determine type
      Widget body;
      if (type == 'Add') {
        body = TextBox(
          placeholder: 'GitHub or npm URL',
          controller: controller,
        );
      } else if (type == 'Update') {
        body = packages == null
            ? Container()
            : Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '${packages.length == 1 ? 'Package' : 'Packages'} currently eligible for update listed below will be updated.',
                    style: const TextStyle(fontSize: 16),
                  ),
                  for (Map<String, dynamic> pack in packages)
                    Text(
                        pack['name']) // CHECK IF A PACKAGE CAN BE UDPATED FIRST
                ],
              );
      } else if (type == 'Delete') {
        body = packages == null
            ? Container()
            : Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'If you delete ${packages.length == 1 ? 'this package' : 'these packages'}, you won\'t be able to recover ${packages.length == 1 ? 'it' : 'them'}. Do you want to delete ${packages.length == 1 ? 'it' : 'them'}?',
                    style: const TextStyle(fontSize: 16),
                  ),
                  for (Map<String, dynamic> pack in packages) Text(pack['name'])
                ],
              );
      } else {
        body = Text('Invalid dialog type');
      }
      // Dialog
      return ContentDialog(
        title: Text('$type package'),
        content: StreamBuilder<bool>(
            stream: isWorkingStream.stream,
            builder: (context, snapshot) {
              return (snapshot.hasData && snapshot.data == true)
                  ? SizedBox(
                      height: 32, width: double.infinity, child: ProgressBar())
                  : body;
            }),
        actions: [
          StreamBuilder<bool>(
              stream: isWorkingStream.stream,
              builder: (context, snapshot) {
                return FilledButton(
                  onPressed: (snapshot.hasData && snapshot.data == true)
                      ? null
                      : () async {
                          isWorkingStream.add(true);
                          if (type == 'Add') {
                            APICaller.addPackage(url: controller.text);
                          } else if (type == 'Update') {
                            APICaller.updatePackages();
                          } else if (type == 'Delete') {
                            APICaller.deletePackages();
                          }
                          await Future.delayed(Duration(seconds: 2))
                              .then((value) => Navigator.pop(context, true));
                        },
                  child: Text(type),
                );
              }),
          StreamBuilder<bool>(
              stream: isWorkingStream.stream,
              builder: (context, snapshot) {
                return Button(
                  onPressed: (snapshot.hasData && snapshot.data == true)
                      ? null
                      : () => Navigator.pop(context, false),
                  child: const Text('Cancel'),
                );
              }),
        ],
      );
    },
  );
  return result ?? false;
}

Future<String> showPropertiesDialog(BuildContext context,
    {required Map<String, dynamic> data}) async {
  final result = await showDialog<String>(
    context: context,
    builder: (context) => ContentDialog(
      style: const ContentDialogThemeData(bodyStyle: TextStyle(fontSize: 20)),
      title: const Text('Properties'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            propertyRow(name: 'Name', value: data['name'].toString()),
            propertyRow(name: 'ID', value: data['id'].toString()),
            propertyRow(
                name: 'Rating',
                value: double.parse('${data['rating']}').toStringAsFixed(2)),
            propertyRow(name: 'Version', value: data['version'].toString()),
            propertyRow(name: 'Description', value: data['info'].toString()),
            propertyRow(name: 'URL', value: data['url'].toString()),
          ],
        ),
      ),
      actions: [
        FilledButton(
          child: const Text('Close'),
          onPressed: () => Navigator.pop(context, 'canceled'),
        ),
      ],
    ),
  );
  return result ?? 'canceled';
}

Widget propertyRow({required String name, required String value}) {
  return Container(
    decoration: BoxDecoration(
        color: const Color.fromARGB(255, 235, 235, 235),
        borderRadius: BorderRadius.circular(7)),
    padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
    margin: const EdgeInsets.all(5),
    child: Column(
      children: [
        Padding(
          padding: EdgeInsets.only(bottom: (value.length > 20) ? 7 : 0),
          child: Row(
            children: [
              Text(
                style: const TextStyle(fontWeight: FontWeight.bold),
                name,
                textAlign: TextAlign.start,
              ),
              const Spacer(),
              Text(
                value.length > 20 ? '' : value,
                textAlign: TextAlign.end,
              )
            ],
          ),
        ),
        if (value.length > 20)
          GestureDetector(
            onTap: () {
              if (name == 'URL') {
                // TODO
              }
            },
            child: Text(
              style: TextStyle(
                  fontSize: 14,
                  color: (name == 'URL') ? Colors.blue : Colors.black,
                  decoration: (name == 'URL')
                      ? TextDecoration.underline
                      : TextDecoration.none),
              overflow: TextOverflow.fade,
              softWrap: true,
              maxLines: 6,
              value,
            ),
          )
      ],
    ),
  );
}
