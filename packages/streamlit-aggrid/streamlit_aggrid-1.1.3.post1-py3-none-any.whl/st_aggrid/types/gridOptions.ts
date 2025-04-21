//import type { AgChartTheme, AgChartThemeOverrides } from 'ag-charts-types';
//import type { AdvancedFilterBuilderVisibleChangedEvent, AsyncTransactionsFlushedEvent, BodyScrollEndEvent, BodyScrollEvent, CellClickedEvent, CellContextMenuEvent, CellDoubleClickedEvent, CellEditRequestEvent, CellEditingStartedEvent, CellEditingStoppedEvent, CellFocusedEvent, CellKeyDownEvent, CellMouseDownEvent, CellMouseOutEvent, CellMouseOverEvent, CellSelectionChangedEvent, CellSelectionDeleteEndEvent, CellSelectionDeleteStartEvent, CellValueChangedEvent, ChartCreatedEvent, ChartDestroyedEvent, ChartOptionsChangedEvent, ChartRangeSelectionChangedEvent, ColumnEverythingChangedEvent, ColumnGroupOpenedEvent, ColumnHeaderClickedEvent, ColumnHeaderContextMenuEvent, ColumnHeaderMouseLeaveEvent, ColumnHeaderMouseOverEvent, ColumnMenuVisibleChangedEvent, ColumnMovedEvent, ColumnPinnedEvent, ColumnPivotChangedEvent, ColumnPivotModeChangedEvent, ColumnResizedEvent, ColumnRowGroupChangedEvent, ColumnValueChangedEvent, ColumnVisibleEvent, ComponentStateChangedEvent, ContextMenuVisibleChangedEvent, CutEndEvent, CutStartEvent, DisplayedColumnsChangedEvent, DragCancelledEvent, DragStartedEvent, DragStoppedEvent, ExpandOrCollapseAllEvent, FillEndEvent, FillStartEvent, FilterChangedEvent, FilterModifiedEvent, FilterOpenedEvent, FirstDataRenderedEvent, FullWidthCellKeyDownEvent, GridColumnsChangedEvent, GridPreDestroyedEvent, GridReadyEvent, GridSizeChangedEvent, HeaderFocusedEvent, ModelUpdatedEvent, NewColumnsLoadedEvent, PaginationChangedEvent, PasteEndEvent, PasteStartEvent, PinnedRowDataChangedEvent, PivotMaxColumnsExceededEvent, RangeDeleteEndEvent, RangeDeleteStartEvent, RangeSelectionChangedEvent, RedoEndedEvent, RedoStartedEvent, RowClickedEvent, RowDataUpdatedEvent, RowDoubleClickedEvent, RowDragCancelEvent, RowDragEndEvent, RowDragEnterEvent, RowDragLeaveEvent, RowDragMoveEvent, RowEditingStartedEvent, RowEditingStoppedEvent, RowGroupOpenedEvent, RowSelectedEvent, RowValueChangedEvent, SelectionChangedEvent, SortChangedEvent, StateUpdatedEvent, StoreRefreshedEvent, ToolPanelSizeChangedEvent, ToolPanelVisibleChangedEvent, TooltipHideEvent, TooltipShowEvent, UndoEndedEvent, UndoStartedEvent, ViewportChangedEvent, VirtualColumnsChangedEvent, VirtualRowRemovedEvent } from '../events';
//import type { SizeColumnsToContentStrategy, SizeColumnsToFitGridStrategy, SizeColumnsToFitProvidedWidthStrategy } from '../interfaces/autoSize';
//import type { CsvExportParams, ProcessCellForExportParams, ProcessGroupHeaderForExportParams, ProcessHeaderForExportParams } from '../interfaces/exportParams';
//import type { GridState } from '../interfaces/gridState';
//import type { IAdvancedFilterBuilderParams } from '../interfaces/iAdvancedFilterBuilderParams';
//import type { AlignedGrid } from '../interfaces/iAlignedGrid';
//import type { FillOperationParams, FocusGridInnerElementParams, GetChartMenuItemsParams, GetChartToolbarItemsParams, GetContextMenuItemsParams, GetGroupAggFilteringParams, GetGroupIncludeFooterParams, GetGroupIncludeTotalRowParams, GetGroupRowAggParams, GetLocaleTextParams, GetMainMenuItemsParams, GetRowIdParams, GetServerSideGroupLevelParamsParams, InitialGroupOrderComparatorParams, IsApplyServerSideTransactionParams, IsExternalFilterPresentParams, IsFullWidthRowParams, IsGroupOpenByDefaultParams, IsServerSideGroupOpenByDefaultParams, NavigateToNextCellParams, NavigateToNextHeaderParams, PaginationNumberFormatterParams, PostProcessPopupParams, PostSortRowsParams, ProcessDataFromClipboardParams, ProcessRowParams, ProcessUnpinnedColumnsParams, RowHeightParams, SendToClipboardParams, TabToNextCellParams, TabToNextHeaderParams } from '../interfaces/iCallbackParams';
//import type { CellPosition } from '../interfaces/iCellPosition';
//import type { ChartToolPanelsDef, ChartToolbarMenuItemOptions, DefaultChartMenuItem } from '../interfaces/iChartOptions';
//import type { Column } from '../interfaces/iColumn';
//import type { AgGridCommon } from '../interfaces/iCommon';
//import type { IDatasource } from '../interfaces/iDatasource';
//import type { ExcelExportParams, ExcelStyle } from '../interfaces/iExcelCreator';
//import type { HeaderPosition } from '../interfaces/iHeaderPosition';
//import type { ILoadingCellRendererParams } from '../interfaces/iLoadingCellRenderer';
//import type { IRowDragItem } from '../interfaces/iRowDragItem';
//import type { RowModelType } from '../interfaces/iRowModel';
//import type { IRowNode } from '../interfaces/iRowNode';
//import type { IServerSideDatasource } from '../interfaces/iServerSideDatasource';
//import type { SideBarDef } from '../interfaces/iSideBar';
//import type { StatusPanelDef } from '../interfaces/iStatusPanel';
//import type { IViewportDatasource } from '../interfaces/iViewportDatasource';
//import type { DefaultMenuItem, MenuItemDef } from '../interfaces/menuItem';
//import type { Theme } from '../theming/Theme';
//import type { CheckboxSelectionCallback, ColDef, ColGroupDef, ColTypeDef, IAggFunc, SortDirection } from './colDef';
//import type { DataTypeDefinition } from './dataType';

export interface GridOptions<TData = any> {
  statusBar?: {
    statusPanels: StatusPanelDef[];
  };
  sideBar?: SideBarDef | string | string[] | boolean | null;
  suppressContextMenu?: boolean;
  preventDefaultOnContextMenu?: boolean;
  allowContextMenuWithControlKey?: boolean;
  columnMenu?: "legacy" | "new";
  suppressMenuHide?: boolean;
  enableBrowserTooltips?: boolean;
  tooltipTrigger?: "hover" | "focus";
  tooltipShowDelay?: number;
  tooltipHideDelay?: number;
  tooltipMouseTrack?: boolean;
  tooltipShowMode?: "standard" | "whenTruncated";
  tooltipInteraction?: boolean;
  popupParent?: HTMLElement | null;
  copyHeadersToClipboard?: boolean;
  copyGroupHeadersToClipboard?: boolean;
  clipboardDelimiter?: string;
  suppressCopyRowsToClipboard?: boolean;
  suppressCopySingleCellRanges?: boolean;
  suppressLastEmptyLineOnPaste?: boolean;
  suppressClipboardPaste?: boolean;
  suppressClipboardApi?: boolean;
  suppressCutToClipboard?: boolean;
  columnDefs?: (ColDef<TData> | ColGroupDef<TData>)[] | null;
  defaultColDef?: ColDef<TData>;
  defaultColGroupDef?: Partial<ColGroupDef<TData>>;
  columnTypes?: {
    [key: string]: ColTypeDef<TData>;
  };
  dataTypeDefinitions?: {
    [cellDataType: string]: DataTypeDefinition<TData>;
  };
  maintainColumnOrder?: boolean;
  enableStrictPivotColumnOrder?: boolean;
  suppressFieldDotNotation?: boolean;
  headerHeight?: number;
  groupHeaderHeight?: number;
  floatingFiltersHeight?: number;
  pivotHeaderHeight?: number;
  pivotGroupHeaderHeight?: number;
  allowDragFromColumnsToolPanel?: boolean;
  suppressMovableColumns?: boolean;
  suppressColumnMoveAnimation?: boolean;
  suppressMoveWhenColumnDragging?: boolean;
  suppressDragLeaveHidesColumns?: boolean;
  suppressGroupChangesColumnVisibility?:
    | boolean
    | "suppressHideOnGroup"
    | "suppressShowOnUngroup";
  suppressMakeColumnVisibleAfterUnGroup?: boolean;
  suppressRowGroupHidesColumns?: boolean;
  colResizeDefault?: "shift";
  suppressAutoSize?: boolean;
  autoSizePadding?: number;
  skipHeaderOnAutoSize?: boolean;
  autoSizeStrategy?:
    | SizeColumnsToFitGridStrategy
    | SizeColumnsToFitProvidedWidthStrategy
    | SizeColumnsToContentStrategy;
  components?: {
    [p: string]: any;
  };
  editType?: "fullRow";
  singleClickEdit?: boolean;
  suppressClickEdit?: boolean;
  readOnlyEdit?: boolean;
  stopEditingWhenCellsLoseFocus?: boolean;
  enterNavigatesVertically?: boolean;
  enterNavigatesVerticallyAfterEdit?: boolean;
  enableCellEditingOnBackspace?: boolean;
  undoRedoCellEditing?: boolean;
  undoRedoCellEditingLimit?: number;
  defaultCsvExportParams?: CsvExportParams;
  suppressCsvExport?: boolean;
  defaultExcelExportParams?: ExcelExportParams;
  suppressExcelExport?: boolean;
  excelStyles?: ExcelStyle[];
  quickFilterText?: string;
  cacheQuickFilter?: boolean;
  includeHiddenColumnsInQuickFilter?: boolean;
  quickFilterParser?: (quickFilter: string) => string[];
  quickFilterMatcher?: (
    quickFilterParts: string[],
    rowQuickFilterAggregateText: string
  ) => boolean;
  applyQuickFilterBeforePivotOrAgg?: boolean;
  excludeChildrenWhenTreeDataFiltering?: boolean;
  enableAdvancedFilter?: boolean;
  alwaysPassFilter?: (rowNode: IRowNode<TData>) => boolean;
  includeHiddenColumnsInAdvancedFilter?: boolean;
  advancedFilterParent?: HTMLElement | null;
  advancedFilterBuilderParams?: IAdvancedFilterBuilderParams;
  suppressAdvancedFilterEval?: boolean;
  suppressSetFilterByDefault?: boolean;
  enableCharts?: boolean;
  chartThemes?: string[];
  customChartThemes?: {
    [name: string]: AgChartTheme;
  };
  chartThemeOverrides?: AgChartThemeOverrides;
  chartToolPanelsDef?: ChartToolPanelsDef;
  chartMenuItems?:
    | (DefaultChartMenuItem | MenuItemDef)[]
    | GetChartMenuItems<TData>;
  loadingCellRenderer?: any;
  loadingCellRendererParams?: any;
  loadingCellRendererSelector?: LoadingCellRendererSelectorFunc<TData>;
  localeText?: {
    [key: string]: string;
  };
  masterDetail?: boolean;
  keepDetailRows?: boolean;
  keepDetailRowsCount?: number;
  detailCellRenderer?: any;
  detailCellRendererParams?: any;
  detailRowHeight?: number;
  detailRowAutoHeight?: boolean;
  context?: any;
  dragAndDropImageComponent?: any;
  dragAndDropImageComponentParams?: any;
  alignedGrids?: AlignedGrid[] | (() => AlignedGrid[]);
  tabIndex?: number;
  rowBuffer?: number;
  valueCache?: boolean;
  valueCacheNeverExpires?: boolean;
  enableCellExpressions?: boolean;
  suppressTouch?: boolean;
  suppressFocusAfterRefresh?: boolean;
  suppressBrowserResizeObserver?: boolean;
  suppressPropertyNamesCheck?: boolean;
  suppressChangeDetection?: boolean;
  debug?: boolean;
  loading?: boolean;
  overlayLoadingTemplate?: string;
  loadingOverlayComponent?: any;
  loadingOverlayComponentParams?: any;
  suppressLoadingOverlay?: boolean;
  overlayNoRowsTemplate?: string;
  noRowsOverlayComponent?: any;
  noRowsOverlayComponentParams?: any;
  suppressNoRowsOverlay?: boolean;
  pagination?: boolean;
  paginationPageSize?: number;
  paginationPageSizeSelector?: number[] | boolean;
  paginationAutoPageSize?: boolean;
  paginateChildRows?: boolean;
  suppressPaginationPanel?: boolean;
  pivotMode?: boolean;
  pivotPanelShow?: "always" | "onlyWhenPivoting" | "never";
  pivotMaxGeneratedColumns?: number;
  pivotDefaultExpanded?: number;
  pivotColumnGroupTotals?: "before" | "after";
  pivotRowTotals?: "before" | "after";
  pivotSuppressAutoColumn?: boolean;
  suppressExpandablePivotGroups?: boolean;
  functionsReadOnly?: boolean;
  aggFuncs?: {
    [key: string]: IAggFunc<TData>;
  };
  suppressAggFuncInHeader?: boolean;
  alwaysAggregateAtRootLevel?: boolean;
  aggregateOnlyChangedColumns?: boolean;
  suppressAggFilteredOnly?: boolean;
  removePivotHeaderRowWhenSingleValueColumn?: boolean;
  animateRows?: boolean;
  cellFlashDuration?: number;
  cellFadeDuration?: number;
  allowShowChangeAfterFilter?: boolean;
  domLayout?: DomLayoutType;
  ensureDomOrder?: boolean;
  enableRtl?: boolean;
  suppressColumnVirtualisation?: boolean;
  suppressMaxRenderedRowRestriction?: boolean;
  suppressRowVirtualisation?: boolean;
  rowDragManaged?: boolean;
  suppressRowDrag?: boolean;
  suppressMoveWhenRowDragging?: boolean;
  rowDragEntireRow?: boolean;
  rowDragMultiRow?: boolean;
  rowDragText?: (params: IRowDragItem, dragItemCount: number) => string;
  fullWidthCellRenderer?: any;
  fullWidthCellRendererParams?: any;
  embedFullWidthRows?: boolean;
  groupDisplayType?: RowGroupingDisplayType;
  groupDefaultExpanded?: number;
  autoGroupColumnDef?: ColDef<TData>;
  groupMaintainOrder?: boolean;
  groupSelectsChildren?: boolean;
  groupLockGroupColumns?: number;
  groupAggFiltering?: boolean | IsRowFilterable<TData>;
  groupTotalRow?: "top" | "bottom" | UseGroupTotalRow<TData>;
  grandTotalRow?: "top" | "bottom";
  suppressStickyTotalRow?: boolean | "grand" | "group";
  groupSuppressBlankHeader?: boolean;
  groupSelectsFiltered?: boolean;
  showOpenedGroup?: boolean;
  groupHideParentOfSingleChild?: boolean | "leafGroupsOnly";
  groupRemoveSingleChildren?: boolean;
  groupRemoveLowestSingleChildren?: boolean;
  groupHideOpenParents?: boolean;
  groupAllowUnbalanced?: boolean;
  rowGroupPanelShow?: "always" | "onlyWhenGrouping" | "never";
  groupRowRenderer?: any;
  groupRowRendererParams?: any;
  treeData?: boolean;
  rowGroupPanelSuppressSort?: boolean;
  suppressGroupRowsSticky?: boolean;
  pinnedTopRowData?: any[];
  pinnedBottomRowData?: any[];
  rowModelType?: RowModelType;
  rowData?: TData[] | null;
  asyncTransactionWaitMillis?: number;
  suppressModelUpdateAfterUpdateTransaction?: boolean;
  datasource?: IDatasource;
  cacheOverflowSize?: number;
  infiniteInitialRowCount?: number;
  serverSideInitialRowCount?: number;
  suppressServerSideFullWidthLoadingRow?: boolean;
  cacheBlockSize?: number;
  maxBlocksInCache?: number;
  maxConcurrentDatasourceRequests?: number;
  blockLoadDebounceMillis?: number;
  purgeClosedRowNodes?: boolean;
  serverSideDatasource?: IServerSideDatasource;
  serverSideSortAllLevels?: boolean;
  serverSideEnableClientSideSort?: boolean;
  serverSideOnlyRefreshFilteredGroups?: boolean;
  serverSidePivotResultFieldSeparator?: string;
  viewportDatasource?: IViewportDatasource;
  viewportRowModelPageSize?: number;
  viewportRowModelBufferSize?: number;
  alwaysShowHorizontalScroll?: boolean;
  alwaysShowVerticalScroll?: boolean;
  debounceVerticalScrollbar?: boolean;
  suppressHorizontalScroll?: boolean;
  suppressScrollOnNewData?: boolean;
  suppressScrollWhenPopupsAreOpen?: boolean;
  suppressAnimationFrame?: boolean;
  suppressMiddleClickScrolls?: boolean;
  suppressPreventDefaultOnMouseWheel?: boolean;
  scrollbarWidth?: number;
  rowSelection?: RowSelectionOptions<TData> | "single" | "multiple";
  cellSelection?: boolean | CellSelectionOptions<TData>;
  rowMultiSelectWithClick?: boolean;
  suppressRowDeselection?: boolean;
  suppressRowClickSelection?: boolean;
  suppressCellFocus?: boolean;
  suppressHeaderFocus?: boolean;
  selectionColumnDef?: SelectionColumnDef;
  suppressMultiRangeSelection?: boolean;
  enableCellTextSelection?: boolean;
  enableRangeSelection?: boolean;
  enableRangeHandle?: boolean;
  enableFillHandle?: boolean;
  fillHandleDirection?: "x" | "y" | "xy";
  suppressClearOnFillReduction?: boolean;
  sortingOrder?: SortDirection[];
  accentedSort?: boolean;
  unSortIcon?: boolean;
  suppressMultiSort?: boolean;
  alwaysMultiSort?: boolean;
  multiSortKey?: "ctrl";
  suppressMaintainUnsortedOrder?: boolean;
  icons?: {
    [key: string]: ((...args: any[]) => any) | string;
  };
  rowHeight?: number;
  rowStyle?: RowStyle;
  rowClass?: string | string[];
  rowClassRules?: RowClassRules<TData>;
  suppressRowHoverHighlight?: boolean;
  suppressRowTransform?: boolean;
  columnHoverHighlight?: boolean;
  gridId?: string;
  deltaSort?: boolean;
  treeDataDisplayType?: TreeDataDisplayType;
  enableGroupEdit?: boolean;
  initialState?: GridState;
  reactiveCustomComponents?: boolean;
  theme?: Theme | "legacy";
  loadThemeGoogleFonts?: boolean;
  getContextMenuItems?: GetContextMenuItems<TData>;
  getMainMenuItems?: GetMainMenuItems<TData>;
  postProcessPopup?: (params: PostProcessPopupParams<TData>) => void;
  processUnpinnedColumns?: (
    params: ProcessUnpinnedColumnsParams<TData>
  ) => Column[];
  processCellForClipboard?: (params: ProcessCellForExportParams<TData>) => any;
  processHeaderForClipboard?: (
    params: ProcessHeaderForExportParams<TData>
  ) => any;
  processGroupHeaderForClipboard?: (
    params: ProcessGroupHeaderForExportParams<TData>
  ) => any;
  processCellFromClipboard?: (params: ProcessCellForExportParams<TData>) => any;
  sendToClipboard?: (params: SendToClipboardParams<TData>) => void;
  processDataFromClipboard?: (
    params: ProcessDataFromClipboardParams<TData>
  ) => string[][] | null;
  isExternalFilterPresent?: (
    params: IsExternalFilterPresentParams<TData>
  ) => boolean;
  doesExternalFilterPass?: (node: IRowNode<TData>) => boolean;
  getChartToolbarItems?: GetChartToolbarItems;
  createChartContainer?: (params: ChartRefParams<TData>) => void;
  focusGridInnerElement?: (
    params: FocusGridInnerElementParams<TData>
  ) => boolean;
  navigateToNextHeader?: (
    params: NavigateToNextHeaderParams<TData>
  ) => HeaderPosition | null;
  tabToNextHeader?: (
    params: TabToNextHeaderParams<TData>
  ) => HeaderPosition | boolean;
  navigateToNextCell?: (
    params: NavigateToNextCellParams<TData>
  ) => CellPosition | null;
  tabToNextCell?: (
    params: TabToNextCellParams<TData>
  ) => CellPosition | boolean;
  getLocaleText?: (params: GetLocaleTextParams<TData>) => string;
  getDocument?: () => Document;
  paginationNumberFormatter?: (
    params: PaginationNumberFormatterParams<TData>
  ) => string;
  getGroupRowAgg?: (params: GetGroupRowAggParams<TData>) => any;
  isGroupOpenByDefault?: (params: IsGroupOpenByDefaultParams<TData>) => boolean;
  initialGroupOrderComparator?: (
    params: InitialGroupOrderComparatorParams<TData>
  ) => number;
  processPivotResultColDef?: (colDef: ColDef<TData>) => void;
  processPivotResultColGroupDef?: (colGroupDef: ColGroupDef<TData>) => void;
  getDataPath?: GetDataPath<TData>;
  getChildCount?: (dataItem: any) => number;
  getServerSideGroupLevelParams?: (
    params: GetServerSideGroupLevelParamsParams
  ) => ServerSideGroupLevelParams;
  isServerSideGroupOpenByDefault?: (
    params: IsServerSideGroupOpenByDefaultParams
  ) => boolean;
  isApplyServerSideTransaction?: IsApplyServerSideTransaction;
  isServerSideGroup?: IsServerSideGroup;
  getServerSideGroupKey?: GetServerSideGroupKey;
  getBusinessKeyForNode?: (node: IRowNode<TData>) => string;
  getRowId?: GetRowIdFunc<TData>;
  resetRowDataOnUpdate?: boolean;
  processRowPostCreate?: (params: ProcessRowParams<TData>) => void;
  isRowSelectable?: IsRowSelectable<TData>;
  isRowMaster?: IsRowMaster<TData>;
  fillOperation?: (params: FillOperationParams<TData>) => any;
  postSortRows?: (params: PostSortRowsParams<TData>) => void;
  getRowStyle?: (params: RowClassParams<TData>) => RowStyle | undefined;
  getRowClass?: (
    params: RowClassParams<TData>
  ) => string | string[] | undefined;
  getRowHeight?: (params: RowHeightParams<TData>) => number | undefined | null;
  isFullWidthRow?: (params: IsFullWidthRowParams<TData>) => boolean;
  onToolPanelVisibleChanged?(event: ToolPanelVisibleChangedEvent<TData>): void;
  onToolPanelSizeChanged?(event: ToolPanelSizeChangedEvent<TData>): void;
  onColumnMenuVisibleChanged?(
    event: ColumnMenuVisibleChangedEvent<TData>
  ): void;
  onContextMenuVisibleChanged?(
    event: ContextMenuVisibleChangedEvent<TData>
  ): void;
  onCutStart?(event: CutStartEvent<TData>): void;
  onCutEnd?(event: CutEndEvent<TData>): void;
  onPasteStart?(event: PasteStartEvent<TData>): void;
  onPasteEnd?(event: PasteEndEvent<TData>): void;
  onColumnVisible?(event: ColumnVisibleEvent<TData>): void;
  onColumnPinned?(event: ColumnPinnedEvent<TData>): void;
  onColumnResized?(event: ColumnResizedEvent<TData>): void;
  onColumnMoved?(event: ColumnMovedEvent<TData>): void;
  onColumnValueChanged?(event: ColumnValueChangedEvent<TData>): void;
  onColumnPivotModeChanged?(event: ColumnPivotModeChangedEvent<TData>): void;
  onColumnPivotChanged?(event: ColumnPivotChangedEvent<TData>): void;
  onColumnGroupOpened?(event: ColumnGroupOpenedEvent<TData>): void;
  onNewColumnsLoaded?(event: NewColumnsLoadedEvent<TData>): void;
  onGridColumnsChanged?(event: GridColumnsChangedEvent<TData>): void;
  onDisplayedColumnsChanged?(event: DisplayedColumnsChangedEvent<TData>): void;
  onVirtualColumnsChanged?(event: VirtualColumnsChangedEvent<TData>): void;
  onColumnEverythingChanged?(event: ColumnEverythingChangedEvent<TData>): void;
  onColumnHeaderMouseOver?(event: ColumnHeaderMouseOverEvent<TData>): void;
  onColumnHeaderMouseLeave?(event: ColumnHeaderMouseLeaveEvent<TData>): void;
  onColumnHeaderClicked?(event: ColumnHeaderClickedEvent<TData>): void;
  onColumnHeaderContextMenu?(event: ColumnHeaderContextMenuEvent<TData>): void;
  onComponentStateChanged?(event: ComponentStateChangedEvent<TData>): void;
  onCellValueChanged?(event: CellValueChangedEvent<TData>): void;
  onCellEditRequest?(event: CellEditRequestEvent<TData>): void;
  onRowValueChanged?(event: RowValueChangedEvent<TData>): void;
  onCellEditingStarted?(event: CellEditingStartedEvent<TData>): void;
  onCellEditingStopped?(event: CellEditingStoppedEvent<TData>): void;
  onRowEditingStarted?(event: RowEditingStartedEvent<TData>): void;
  onRowEditingStopped?(event: RowEditingStoppedEvent<TData>): void;
  onUndoStarted?(event: UndoStartedEvent<TData>): void;
  onUndoEnded?(event: UndoEndedEvent<TData>): void;
  onRedoStarted?(event: RedoStartedEvent<TData>): void;
  onRedoEnded?(event: RedoEndedEvent<TData>): void;
  onCellSelectionDeleteStart?(
    event: CellSelectionDeleteStartEvent<TData>
  ): void;
  onCellSelectionDeleteEnd?(event: CellSelectionDeleteEndEvent<TData>): void;
  onRangeDeleteStart?(event: RangeDeleteStartEvent<TData>): void;
  onRangeDeleteEnd?(event: RangeDeleteEndEvent<TData>): void;
  onFillStart?(event: FillStartEvent<TData>): void;
  onFillEnd?(event: FillEndEvent<TData>): void;
  onFilterOpened?(event: FilterOpenedEvent<TData>): void;
  onFilterChanged?(event: FilterChangedEvent<TData>): void;
  onFilterModified?(event: FilterModifiedEvent<TData>): void;
  onAdvancedFilterBuilderVisibleChanged?(
    event: AdvancedFilterBuilderVisibleChangedEvent<TData>
  ): void;
  onChartCreated?(event: ChartCreatedEvent<TData>): void;
  onChartRangeSelectionChanged?(
    event: ChartRangeSelectionChangedEvent<TData>
  ): void;
  onChartOptionsChanged?(event: ChartOptionsChangedEvent<TData>): void;
  onChartDestroyed?(event: ChartDestroyedEvent<TData>): void;
  onCellKeyDown?(
    event: CellKeyDownEvent<TData> | FullWidthCellKeyDownEvent<TData>
  ): void;
  onGridReady?(event: GridReadyEvent<TData>): void;
  onGridPreDestroyed?(event: GridPreDestroyedEvent<TData>): void;
  onFirstDataRendered?(event: FirstDataRenderedEvent<TData>): void;
  onGridSizeChanged?(event: GridSizeChangedEvent<TData>): void;
  onModelUpdated?(event: ModelUpdatedEvent<TData>): void;
  onVirtualRowRemoved?(event: VirtualRowRemovedEvent<TData>): void;
  onViewportChanged?(event: ViewportChangedEvent<TData>): void;
  onBodyScroll?(event: BodyScrollEvent<TData>): void;
  onBodyScrollEnd?(event: BodyScrollEndEvent<TData>): void;
  onDragStarted?(event: DragStartedEvent<TData>): void;
  onDragStopped?(event: DragStoppedEvent<TData>): void;
  onDragCancelled?(event: DragCancelledEvent<TData>): void;
  onStateUpdated?(event: StateUpdatedEvent<TData>): void;
  onPaginationChanged?(event: PaginationChangedEvent<TData>): void;
  onRowDragEnter?(event: RowDragEnterEvent<TData>): void;
  onRowDragMove?(event: RowDragMoveEvent<TData>): void;
  onRowDragLeave?(event: RowDragLeaveEvent<TData>): void;
  onRowDragEnd?(event: RowDragEndEvent<TData>): void;
  onRowDragCancel?(event: RowDragCancelEvent<TData>): void;
  onColumnRowGroupChanged?(event: ColumnRowGroupChangedEvent<TData>): void;
  onRowGroupOpened?(event: RowGroupOpenedEvent<TData>): void;
  onExpandOrCollapseAll?(event: ExpandOrCollapseAllEvent<TData>): void;
  onPivotMaxColumnsExceeded?(event: PivotMaxColumnsExceededEvent<TData>): void;
  onPinnedRowDataChanged?(event: PinnedRowDataChangedEvent<TData>): void;
  onRowDataUpdated?(event: RowDataUpdatedEvent<TData>): void;
  onAsyncTransactionsFlushed?(
    event: AsyncTransactionsFlushedEvent<TData>
  ): void;
  onStoreRefreshed?(event: StoreRefreshedEvent<TData>): void;
  onHeaderFocused?(event: HeaderFocusedEvent<TData>): void;
  onCellClicked?(event: CellClickedEvent<TData>): void;
  onCellDoubleClicked?(event: CellDoubleClickedEvent<TData>): void;
  onCellFocused?(event: CellFocusedEvent<TData>): void;
  onCellMouseOver?(event: CellMouseOverEvent<TData>): void;
  onCellMouseOut?(event: CellMouseOutEvent<TData>): void;
  onCellMouseDown?(event: CellMouseDownEvent<TData>): void;
  onRowClicked?(event: RowClickedEvent<TData>): void;
  onRowDoubleClicked?(event: RowDoubleClickedEvent<TData>): void;
  onRowSelected?(event: RowSelectedEvent<TData>): void;
  onSelectionChanged?(event: SelectionChangedEvent<TData>): void;
  onCellContextMenu?(event: CellContextMenuEvent<TData>): void;
  onRangeSelectionChanged?(event: RangeSelectionChangedEvent<TData>): void;
  onCellSelectionChanged?(event: CellSelectionChangedEvent<TData>): void;
  onTooltipShow?(event?: TooltipShowEvent<TData>): void;
  onTooltipHide?(event?: TooltipHideEvent<TData>): void;
  onSortChanged?(event: SortChangedEvent<TData>): void;
}
export type RowGroupingDisplayType =
  | "singleColumn"
  | "multipleColumns"
  | "groupRows"
  | "custom";
export type TreeDataDisplayType = "auto" | "custom";
export interface GetDataPath<TData = any> {
  (data: TData): string[];
}
export interface IsServerSideGroup {
  (dataItem: any): boolean;
}
export interface IsRowFilterable<TData = any> {
  (params: GetGroupAggFilteringParams<TData>): boolean;
}
export interface UseGroupFooter<TData = any> {
  (params: GetGroupIncludeFooterParams<TData>): boolean;
}
export interface UseGroupTotalRow<TData = any> {
  (params: GetGroupIncludeTotalRowParams<TData>): "top" | "bottom" | undefined;
}
export interface IsApplyServerSideTransaction {
  (params: IsApplyServerSideTransactionParams): boolean;
}
export interface GetServerSideGroupKey {
  (dataItem: any): string;
}
export interface IsRowMaster<TData = any> {
  (dataItem: TData): boolean;
}
export interface IsRowSelectable<TData = any> {
  (node: IRowNode<TData>): boolean;
}
export interface RowClassRules<TData = any> {
  [cssClassName: string]: ((params: RowClassParams<TData>) => boolean) | string;
}
export interface RowStyle {
  [cssProperty: string]: string | number;
}
export interface RowClassParams<TData = any, TContext = any>
  extends AgGridCommon<TData, TContext> {
  data: TData | undefined;
  node: IRowNode<TData>;
  rowIndex: number;
}
type MenuCallbackReturn<
  TMenuItem extends string,
  TData = any,
  TContext = any,
> = (TMenuItem | MenuItemDef<TData, TContext>)[];
export interface GetContextMenuItems<TData = any, TContext = any> {
  (
    params: GetContextMenuItemsParams<TData, TContext>
  ):
    | MenuCallbackReturn<DefaultMenuItem, TData, TContext>
    | Promise<MenuCallbackReturn<DefaultMenuItem, TData, TContext>>;
}
export interface GetChartToolbarItems {
  (params: GetChartToolbarItemsParams): ChartToolbarMenuItemOptions[];
}
export interface GetMainMenuItems<TData = any, TContext = any> {
  (
    params: GetMainMenuItemsParams<TData, TContext>
  ): MenuCallbackReturn<DefaultMenuItem, TData, TContext>;
}
export interface GetChartMenuItems<TData = any, TContext = any> {
  (
    params: GetChartMenuItemsParams<TData, TContext>
  ): MenuCallbackReturn<DefaultChartMenuItem, TData, TContext>;
}
export interface GetRowNodeIdFunc<TData = any> {
  (data: TData): string;
}
export interface GetRowIdFunc<TData = any> {
  (params: GetRowIdParams<TData>): string;
}
export interface ChartRef {
  chartId: string;
  chart: any;
  chartElement: HTMLElement;
  destroyChart: () => void;
  focusChart: () => void;
}
export interface ChartRefParams<TData = any>
  extends AgGridCommon<TData, any>,
    ChartRef {}
export interface ServerSideGroupLevelParams {
  maxBlocksInCache?: number;
  cacheBlockSize?: number;
}
export interface ServerSideStoreParams extends ServerSideGroupLevelParams {}
export interface LoadingCellRendererSelectorFunc<TData = any> {
  (
    params: ILoadingCellRendererParams<TData>
  ): LoadingCellRendererSelectorResult | undefined;
}
export interface LoadingCellRendererSelectorResult {
  component?: any;
  params?: any;
}
export type DomLayoutType = "normal" | "autoHeight" | "print";
export interface CellSelectionOptions<TData = any> {
  suppressMultiRanges?: boolean;
  handle?: RangeHandleOptions | FillHandleOptions<TData>;
}
export interface RangeHandleOptions {
  mode: "range";
}
export interface FillHandleOptions<TData = any> {
  mode: "fill";
  suppressClearOnFillReduction?: boolean;
  direction?: "x" | "y" | "xy";
  setFillValue?: <TContext = any>(
    params: FillOperationParams<TData, TContext>
  ) => any;
}
export type RowSelectionOptions<TData = any, TValue = any> =
  | SingleRowSelectionOptions<TData, TValue>
  | MultiRowSelectionOptions<TData>;
interface CommonRowSelectionOptions<TData = any, TValue = any> {
  enableClickSelection?: boolean | "enableDeselection" | "enableSelection";
  checkboxes?: boolean | CheckboxSelectionCallback<TData, TValue>;
  checkboxLocation?: CheckboxLocation;
  hideDisabledCheckboxes?: boolean;
  isRowSelectable?: IsRowSelectable<TData>;
  copySelectedRows?: boolean;
  enableSelectionWithoutKeys?: boolean;
}
export interface SingleRowSelectionOptions<TData = any, TValue = any>
  extends CommonRowSelectionOptions<TData, TValue> {
  mode: "singleRow";
}
export interface MultiRowSelectionOptions<TData = any, TValue = any>
  extends CommonRowSelectionOptions<TData, TValue> {
  mode: "multiRow";
  groupSelects?: GroupSelectionMode;
  selectAll?: SelectAllMode;
  headerCheckbox?: boolean;
}
export type SelectionColumnDef = Pick<
  ColDef,
  | "icons"
  | "suppressNavigable"
  | "suppressKeyboardEvent"
  | "contextMenuItems"
  | "context"
  | "onCellClicked"
  | "onCellContextMenu"
  | "onCellDoubleClicked"
  | "onCellValueChanged"
  | "headerTooltip"
  | "headerClass"
  | "headerComponent"
  | "headerComponentParams"
  | "mainMenuItems"
  | "suppressHeaderContextMenu"
  | "suppressHeaderMenuButton"
  | "suppressHeaderKeyboardEvent"
  | "pinned"
  | "lockPinned"
  | "initialPinned"
  | "cellAriaRole"
  | "cellStyle"
  | "cellClass"
  | "cellClassRules"
  | "cellRenderer"
  | "cellRendererParams"
  | "cellRendererSelector"
  | "rowDrag"
  | "rowDragText"
  | "dndSource"
  | "dndSourceOnRowDrag"
  | "sortable"
  | "sort"
  | "initialSort"
  | "sortIndex"
  | "initialSortIndex"
  | "sortingOrder"
  | "unSortIcon"
  | "tooltipField"
  | "tooltipValueGetter"
  | "tooltipComponent"
  | "tooltipComponentParams"
  | "width"
  | "initialWidth"
  | "maxWidth"
  | "minWidth"
  | "flex"
  | "initialFlex"
  | "resizable"
  | "suppressSizeToFit"
  | "suppressAutoSize"
>;
export type GroupSelectionMode = "self" | "descendants" | "filteredDescendants";
export type SelectAllMode = "all" | "filtered" | "currentPage";
export type RowSelectionMode = RowSelectionOptions["mode"];
export type CheckboxLocation = "selectionColumn" | "autoGroupColumn";
export {};
