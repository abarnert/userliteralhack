# userliteralhack
A hack to provide user-defined literals

Any number token followed by a name token is transformed into a call
to a user literal function.

For example:

 * `1.2d` becomes `user_literal_d('1.2')`
 * `1dec` becomes `user_literal_dec('1.2')`
 * `0x1decimal` becomes `user_literal_imal('0x1dec')`
 
