# ClipGraphExtract
- An example repo for adding the tool to the top-level app and using an OpenDB-C++ API for DAC 2020 tutorial 9.
- The base sources are copied from [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD) repo, commit: [7156dc](https://github.com/The-OpenROAD-Project/OpenROAD/commit/7156dc41b0be75e9090b456103a2a1510913a4d2). Unessential repos are removed to be compiled well in other environments.
- Please read the [doc/OpenRoadArch.md](https://github.com/The-OpenROAD-Project/OpenROAD/blob/master/doc/OpenRoadArch.md) to understand the requirement. The ClipGraphExtract follows the OpenRoadArch.md manual.

## ClipGraphExtract Flow
| <img src="/doc/clique-star-v2.png" width=600px> |
|:--:|
| Clique and star net decomposition example |
- In OpenROAD app, read_lef and read_def command will populate the OpenDB's data structure.
- Using OpenDB's C++ API, save all instances' bbox to Boost/RTree structure. 
- Send a region query to RTree to extract related instances using the clips' coordinates.
- Generate clip graph's clique/star net models as text file (e.g. edges list) for graph neural network models.

## File Structure
-  include/openroad/  
    - public headers location of OpenROAD.

- src/ 
    - OpenROAD source code files. The tools source code should be located here. 
  
- src/ClipGraphExtractor/src/  
    - source code location of ClipGraphExtractor.
  
- src/ClipGraphExtractor/include/clip_graph_ext/  
    - public headers location of ClipGraphExtractor.
  

## Implementation Details
### OpenDB C++ API
- All the OpenDB reference is in the OpenDB's public header [(OpenDB/include/opendb/db.h)](https://github.com/The-OpenROAD-Project/OpenDB/blob/ebbf56ee8ddb08f9a8da5febafe37691731f2932/include/opendb/db.h). Please check this header file first to understand how the structures are designed.

- Set the OpenDB pointer from Top-level app [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/b451e83d26f6fc867d41a4192f71e9d22be31684/src/ClipGraphExtract/src/MakeClipGraphExtractor.cpp#L30-L31)

      void 
      initClipGraphExtractor(OpenRoad *openroad) 
      {
        Tcl_Interp* tcl_interp = openroad->tclInterp();
        Clipgraphextractor_Init(tcl_interp);
        sta::evalTclInit(tcl_interp, sta::graph_extractor_tcl_inits);
        openroad->getClipGraphExtractor()->setDb(openroad->getDb());
        openroad->getClipGraphExtractor()->setSta(openroad->getSta());
      }
    
- Push instances' location to RTree using dbInst* [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/b451e83d26f6fc867d41a4192f71e9d22be31684/src/ClipGraphExtract/src/clipGraphExtractor.cpp#L74-L80)

      dbBlock* block = db_->getChip()->getBlock();
      for( dbInst* inst : block->getInsts() ) {
        dbBox* bBox = inst->getBBox();
        box b (point(bBox->xMin(), bBox->yMin()), 
                point(bBox->xMax(), bBox->yMax()));
        rTree->insert( make_pair(b, inst) );
      }

- Send region query using given bbox coordinates. [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/b451e83d26f6fc867d41a4192f71e9d22be31684/src/ClipGraphExtract/src/clipGraphExtractor.cpp#L91-L97)

      box queryBox( point(lx, ly), point(ux, uy) );

      vector<value> foundInsts; 
      rTree->query(bgi::intersects(queryBox), 
          std::back_inserter(foundInsts));

      cout << "NumFoundInsts: " << foundInsts.size() << endl;

- Store distinctive instances into hash_set (e.g. std::set<dbInst*>) [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/b451e83d26f6fc867d41a4192f71e9d22be31684/src/ClipGraphExtract/src/clipGraphExtractor.cpp#L99-L103)

      set<odb::dbInst*> instSet;
      for(value& val : foundInsts) {
        odb::dbInst* inst = val.second;
        instSet.insert( inst ); 
      }
      
- Extract distinctive dbITerms from dbInst objects [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/a40d582604b432594aee5a40b9b7a76c56ba3bc0/src/ClipGraphExtract/src/instGraph.cpp#L103-L109)

      for(odb::dbITerm* iTerm : inst->getITerms()) {
        if( iTerm->getSigType() == odb::dbSigType::POWER ||
            iTerm->getSigType() == odb::dbSigType::GROUND ) {
          continue;
        }
        iTermSet.insert(iTerm); 
      }

- Extract distinctive dbNet from dbITerm objects [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/a40d582604b432594aee5a40b9b7a76c56ba3bc0/src/ClipGraphExtract/src/instGraph.cpp#L112-L125)

      // extract Net
      set<odb::dbNet*> netSet;
      for(odb::dbITerm* iTerm : iTermSet) {
        odb::dbNet* net = iTerm->getNet();
        if (!net) { 
          continue;
        }
        if( net->getSigType() == odb::dbSigType::POWER ||
            net->getSigType() == odb::dbSigType::GROUND ||
            net->getSigType() == odb::dbSigType::CLOCK ) {
          continue;
        }
        netSet.insert(net);
      }
      
      
### Adding a Tool
- Write tool's CMakeLists.txt [(src/ClipGraphExtract/CMakeLists.txt)](https://github.com/mgwoo/ClipGraphExtract/blob/master/src/ClipGraphExtract/CMakeLists.txt)
  
- Modify OpenROAD's CMakeLists.txt accordingly [(src/CMakeLists.txt)](https://github.com/mgwoo/ClipGraphExtract/blob/master/src/CMakeLists.txt)

  - [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/0652e635b152500e1a75dc849f318455bd33677f/src/CMakeLists.txt#L21)
  
        set(CLIP_GRAPHEXT_HOME ${PROJECT_SOURCE_DIR}/src/ClipGraphExtract)
        
  - [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/0652e635b152500e1a75dc849f318455bd33677f/src/CMakeLists.txt#L205)
  
        add_subdirectory(ClipGraphExtract)
      
  - [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/0652e635b152500e1a75dc849f318455bd33677f/src/CMakeLists.txt#L242) 
  
        target_link_libraries(openroad
        ...
        ClipGraphExtractor
        ...
        )
- Write an initializing public header inside tool [(Link)](https://github.com/mgwoo/ClipGraphExtract/blob/master/src/ClipGraphExtract/include/clip_graph_ext/MakeClipGraphExtractor.h)

      namespace ord {
      class OpenRoad;

      ClipGraphExtract::ClipGraphExtractor* makeClipGraphExtractor();
      void initClipGraphExtractor(OpenRoad *openroad);
      void deleteClipGraphExtractor(ClipGraphExtract::ClipGraphExtractor *graphext);
      }

- Change OpenRoad.cc and OpenRoad.hh accordinly
  - [include/openroad/OpenRoad.hh](https://github.com/mgwoo/ClipGraphExtract/blob/5d92d9d4d657f8dac25762064c9991b597f9d944/include/openroad/OpenRoad.hh#L61-L63)
  
        // incomplete header
        namespace ClipGraphExtract {
        class ClipGraphExtractor;
        }
        
        ...
        // getter functions
        ClipGraphExtract::ClipGraphExtractor *getClipGraphExtractor() { return clipGraphExt_; }
        ...
        // private variable
        ClipGraphExtract::ClipGraphExtractor *clipGraphExt_;

  - [src/OpenRoad.cc](https://github.com/mgwoo/ClipGraphExtract/blob/5d92d9d4d657f8dac25762064c9991b597f9d944/src/OpenRoad.cc#L100)

        // make
        clipGraphExt_ = makeClipGraphExtractor();
        ...
        // delete
        deleteClipGraphExtractor(clipGraphExt_);
        ...
        // init
        initClipGraphExtractor(this);
        ...
        
- Registering Hidden Tcl Command using SWIG [(src/ClipGraphExtract/src/clipGraphExtract.i)](src/ClipGraphExtract/src/clipGraphExtractor.i)

      // Note that hidden SWIG tcl commands must have *_cmd as a function name.
      void
      graph_extract_cmd(int lx, int ly, int ux, int uy) 
      {
        ClipGraphExtractor* graphExt = getClipGraphExtractor();
        graphExt->extract(lx, ly, ux, uy);
      }


- Registering Visible Tcl Command using OpenSTA Tcl Template [(src/ClipGraphExtract/src/clipGraphExtract.tcl)](src/ClipGraphExtract/src/clipGraphExtractor.tcl)

      // register graph_extract commands in OpenROAD binary.
      sta::define_cmd_args "graph_extract" {
        [-graph_model star/clique]\
        [-edge_weight_model weight]\
        [-out_file fileName]
      }
      
      // function details
      proc graph_extract { args } {
      ...
      // *_cmd SWIG functions can be used in here.
      ...
      }


## How to build/test?
- Build
  - Please follow the build manual in [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD)

        $ mkdir build
        $ cd build
        $ cmake ..
        $ make
      
- Test on ClipGraphExtract

      $ cd src/ClipGraphExtract/test/
      $ ../../../build/src/openroad test.tcl
      
## License
- BSD-3-Clause license. 
- Code found under the subdirectory (e.g., src/OpenSTA) have individual copyright and license declarations at each folder.

