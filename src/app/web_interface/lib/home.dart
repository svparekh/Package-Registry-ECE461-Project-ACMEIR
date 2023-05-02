import 'package:fluent_ui/fluent_ui.dart';

import 'api.dart';
import 'data.dart' show PackageRegistry;
import 'popup.dart' show showPackageDialog, showSuccessFailInfoBar;
import 'database_table.dart' show DatabaseCell, DatabaseTable;
import 'main.dart' show PresetValues;
import 'wavy_bg.dart' show WavingBackground;

class HomePage extends StatefulWidget {
  const HomePage({
    super.key,
    required this.importDataSuccess,
  });
  final bool importDataSuccess;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _searchController = TextEditingController();
  final PackageRegistry _pr = PackageRegistry();
  bool refreshSuccess = false;

  @override
  void initState() {
    refreshSuccess = widget.importDataSuccess;
    super.initState();
  }

  void editSelected(bool addValue, Map<String, dynamic> dataRow) {
    setState(() {
      if (addValue) {
        if (!_pr.selectedData.contains(dataRow)) {
          _pr.selectedData.add(dataRow);
        }
      } else {
        _pr.selectedData.remove(dataRow);
      }
    });
  }

  bool _isAllSelected() {
    for (Map<String, dynamic> row in _pr.filteredData) {
      if (!_pr.selectedData.contains(row)) {
        return false;
      }
    }
    return true;
  }

  @override
  Widget build(BuildContext context) {
    return WavingBackground(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          // Search bar
          Container(
              constraints: const BoxConstraints(maxWidth: 500),
              padding: const EdgeInsets.symmetric(vertical: 10),
              child: AutoSuggestBox(
                placeholder: 'Search',
                noResultsFoundBuilder: (context) {
                  return Container(
                    height: 0,
                  );
                },
                onChanged: (text, reason) {
                  setState(() {
                    _pr.filteredData = _pr.searchData(text);
                  });
                },
                controller: _searchController,
                items: const [],
                style: const TextStyle(fontSize: 16),
                leadingIcon: const Padding(
                  padding: EdgeInsets.all(8),
                  child: Tooltip(
                      message: 'Search packages',
                      child: Icon(FluentIcons.search)),
                ),
              )),
          // Command Bar / Filter options
          Padding(
            padding: const EdgeInsets.only(left: 50, right: 50, bottom: 10),
            child: CommandBar(
              mainAxisAlignment: MainAxisAlignment.end,
              overflowBehavior: CommandBarOverflowBehavior.wrap,
              compactBreakpointWidth: 900,
              primaryItems: [
                CommandBarButton(
                  onPressed: () async {
                    // Call reset method
                    bool result =
                        await showPackageDialog(context, type: 'Reset');
                    if (result) {
                      _onRefresh();
                    }
                  },
                  icon: Tooltip(
                      message: 'Reset app to default state',
                      child: Icon(
                        FluentIcons.reset,
                        color: Colors.red,
                      )),
                  label: Text(
                    "Reset",
                    style: TextStyle(color: Colors.red),
                  ),
                ),
                CommandBarButton(
                  onPressed: _onRefresh,
                  icon: const Tooltip(
                      message: 'Refresh package list',
                      child: Icon(FluentIcons.update_restore)),
                  label: const Text(
                    "Refresh",
                  ),
                ),
                CommandBarButton(
                    onPressed: () async {
                      // Call add method
                      bool result =
                          await showPackageDialog(context, type: 'Add');
                      if (result) {
                        _onRefresh();
                      }
                    },
                    icon: const Tooltip(
                        message: 'Add a new package',
                        child: Icon(FluentIcons.add)),
                    label: const Text(
                      'Add',
                    )),
                CommandBarButton(
                  onPressed: _pr.selectedData.isEmpty
                      ? null
                      : () async {
                          // Call delete method
                          bool result = await showPackageDialog(context,
                              type: 'Delete', packages: _pr.selectedData);
                          if (result) {
                            _onRefresh();
                          }
                        },
                  icon: Tooltip(
                      message: 'Delete the selected packages',
                      child: const Icon(FluentIcons.delete)),
                  label: Text(
                    'Delete${_pr.selectedData.isEmpty ? '' : ' (${_pr.selectedData.length})'}',
                    semanticsLabel: 'Delete selected',
                  ),
                ),
                // CommandBarButton(
                //   onPressed: _pr.selectedData.isEmpty
                //       ? null
                //       : () async {
                //           // Call update method
                //           bool result = await showPackageDialog(context,
                //               type: 'Update', packages: _pr.selectedData);
                //           if (result) {
                //             _onRefresh();
                //           }
                //         },
                //   icon: Tooltip(
                //       message: 'Update the selected packages',
                //       child: const Icon(FluentIcons.download)),
                //   label: Text(
                //     'Update${_pr.selectedData.length <= 1 ? '' : ' All'}',
                //     semanticsLabel: 'Update selected',
                //   ),
                // ),
                const CommandBarSeparator(),
                CommandBarButton(
                  onPressed: () {},
                  icon: DropDownButton(
                    title: const Text(
                      "Sort",
                      semanticsLabel: 'Sort method selection dropdown',
                    ),
                    items: [
                      for (int i = 0; i < PresetValues.columns.length - 1; i++)
                        MenuFlyoutItem(
                          text: Text(PresetValues.columns[i]),
                          onPressed: () {
                            setState(
                              () {
                                _pr.curSortMethod = PresetValues.columns[i];
                                _pr.sortData();
                              },
                            );
                          },
                        )
                    ],
                  ),
                ),
                CommandBarButton(
                    onPressed: () {},
                    icon: Tooltip(
                      message:
                          'Switch sort order between ascending or descending',
                      child: Checkbox(
                        semanticLabel: 'Sort ascending or descending',
                        checked: _pr.isSortAscending,
                        onChanged: (value) {
                          setState(() {
                            _pr.isSortAscending = value!;
                            _pr.sortData();
                          });
                        },
                        style: CheckboxThemeData(
                          checkedIconColor:
                              ButtonState.resolveWith((states) => Colors.white),
                          uncheckedIconColor:
                              ButtonState.resolveWith((states) => Colors.white),
                          checkedDecoration: ButtonState.resolveWith((states) =>
                              BoxDecoration(
                                  borderRadius: BorderRadius.circular(5),
                                  color: Colors.blue)),
                          uncheckedDecoration: ButtonState.resolveWith(
                              (states) => BoxDecoration(
                                  borderRadius: BorderRadius.circular(5),
                                  color: Colors.blue)),
                          icon: _pr.isSortAscending
                              ? FluentIcons.up
                              : FluentIcons.down,
                        ),
                      ),
                    ))
              ],
            ),
          ),
          // Main body
          Expanded(
            child: Container(
              padding: const EdgeInsets.only(
                  bottom: 25, left: 50, right: 50, top: 0),
              child: Container(
                decoration: BoxDecoration(
                    color: PresetValues.offwhite,
                    borderRadius: BorderRadius.circular(15)),
                child: Column(
                  children: [
                    // Column names
                    ListTile(
                      // Select all button
                      leading: Checkbox(
                        style: const CheckboxThemeData(
                            padding: EdgeInsets.all(0),
                            margin: EdgeInsets.all(0)),
                        checked: _isAllSelected(),
                        onChanged: (value) {
                          setState(
                            () {
                              if (value!) {
                                // can't do _pr.selectedData = _pr.filteredData; because object is not copied
                                for (Map<String, dynamic> row
                                    in _pr.filteredData) {
                                  if (!_pr.selectedData.contains(row)) {
                                    _pr.selectedData.add(row);
                                  }
                                }
                              } else {
                                _pr.selectedData = [];
                              }
                            },
                          );
                        },
                      ),
                      title: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(children: [
                          for (int i = 0;
                              i < PresetValues.columns.length - 1;
                              i++)
                            DatabaseCell(
                              width: MediaQuery.of(context).size.width / 5,
                              text: PresetValues.columns[i],
                            )
                        ]),
                      ),
                      trailing: DatabaseCell(
                        text: PresetValues
                            .columns[PresetValues.columns.length - 1],
                        width: PresetValues.trailingSize,
                      ),
                    ),
                    // List of data
                    Expanded(
                      child: (widget.importDataSuccess || refreshSuccess)
                          ? DatabaseTable(
                              data: _pr.filteredData,
                              editSelected: editSelected,
                            )
                          : const Text(
                              'Could not load data. You may be signed out or there may be no packages.'),
                    ),
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }

  _onRefresh() async {
    // Call method to refresh data
    refreshSuccess = await PackageRegistry().importData();
    setState(() {
      _searchController.clear();
    });
  }
}
