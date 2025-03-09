# Setup
- 
    ```sh
    # Create virtual environment and activate it
    uv venv
    source .venv/bin/activate

    # Install dependencies
    uv add "mcp[cli]"
    ```

# Features
- Query coverity issues by category
- Query one coverity object by category
    - struct format example
    ```json
    {
        "type" : "AUTO_CAUSES_COPY",
        "mainEventFilePathname": "/home/scratch.louiliu_vlsi_1/work/nvtools_louiliu_2/nvtools/cad/cadlib/vector/JetBasis/PropertyMap.h",
        "mainEventLineNumber": 230,
        "functionDisplayName" : "auto vectorlib::PropertyMapBase<vectorlib::ParameterPackHelper<vectorlib::DUTInst>, vectorlib::ParameterPackHelper<bool, int, unsigned int, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::deque<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >, std::map<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::vector<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > >, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const, std::vector<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, std::allocator<std::pair<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > > > > > >, std::less<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >::bindCast<vectorlib::DUTInstCastHelper, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const &, vectorlib::DUTInst>(std::function<T2 (T3 const &, T4...)>)::[lambda(vectorlib::DUTInst const &) (instance 1)]::operator ()(vectorlib::DUTInst const &) const",
        "events" : {
            "eventDescription": [
                "This lambda has an unspecified return type. This implies \"auto\" and causes the copy of an object of type \"std::string\".",
                "Use \"-> const auto &\"\"std::string\".",
                "This return statement creates a copy.",
            ],
            "subcategoryLongDescription" : "Using the auto keyword without an & causes a copy."
        }
    }
    ```
- Auto fix by cursor
    - given a category
    - for that category one-by-one
    - use cursor to fix the error
    
# Implement Spec
