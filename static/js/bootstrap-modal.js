/* =========================================================
 * bootstrap-modal.js v2.0.2
 * http://twitter.github.com/bootstrap/javascript.html#modals
 * =========================================================
 * Copyright 2012 Twitter, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================= */


!function( $ ){

  "use strict"

 /* MODAL CLASS DEFINITION
  * ====================== */

  var Modal = function ( content, options ) {
    this.options = options
    this.$element = $(content)
      .delegate('[data-dismiss="modal"]', 'click.dismiss.modal', $.proxy(this.hide, this))
  }

  Modal.prototype = {

      constructor: Modal

    , toggle: function () {
        return this[!this.isShown ? 'show' : 'hide']()
      }

    , show: function () {
        var that = this

        if (this.isShown) return

        $('body').addClass('modal-open')

        this.isShown = true
        this.$element.trigger('show')

        escape.call(this)
        backdrop.call(this, function () {
          var transition = $.support.transition && that.$element.hasClass('fade')

          !that.$element.parent().length && that.$element.appendTo(document.body) //don't move modals dom position

          that.$element
            .show()

          if (transition) {
            that.$element[0].offsetWidth // force reflow
          }

          that.$element.addClass('in')

          transition ?
            that.$element.one($.support.transition.end, function () { that.$element.trigger('shown') }) :
            that.$element.trigger('shown')

        })
      }

    , hide: function ( e ) {
        e && e.preventDefault()

        if (!this.isShown) return

        var that = this
        this.isShown = false

        $('body').removeClass('modal-open')

        escape.call(this)

        this.$element
          .trigger('hide')
          .removeClass('in')

        $.support.transition && this.$element.hasClass('fade') ?
          hideWithTransition.call(this) :
          hideModal.call(this)
      }

  }


 /* MODAL PRIVATE METHODS
  * ===================== */

  function hideWithTransition() {
    var that = this
      , timeout = setTimeout(function () {
          that.$element.off($.support.transition.end)
          hideModal.call(that)
        }, 500)

    this.$element.one($.support.transition.end, function () {
      clearTimeout(timeout)
      hideModal.call(that)
    })
  }

  function hideModal( that ) {
    this.$element
      .hide()
      .trigger('hidden')

    backdrop.call(this)
  }

  function backdrop( callback ) {
    var that = this
      , animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
        .appendTo(document.body)

      if (this.options.backdrop != 'static') {
        this.$backdrop.click($.proxy(this.hide, this))
      }

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      doAnimate ?
        this.$backdrop.one($.support.transition.end, callback) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      $.support.transition && this.$element.hasClass('fade')?
        this.$backdrop.one($.support.transition.end, $.proxy(removeBackdrop, this)) :
        removeBackdrop.call(this)

    } else if (callback) {
      callback()
    }
  }

  function removeBackdrop() {
    this.$backdrop.remove()
    this.$backdrop = null
  }

  function escape() {
    var that = this
    if (this.isShown && this.options.keyboard) {
      $(document).on('keyup.dismiss.modal', function ( e ) {
        e.which == 27 && that.hide()
      })
    } else if (!this.isShown) {
      $(document).off('keyup.dismiss.modal')
    }
  }


 /* MODAL PLUGIN DEFINITION
  * ======================= */

  $.fn.modal = function ( option ) {
    return this.each(function () {
      var $this = $(this)
        , data = $this.data('modal')
        , options = $.extend({}, $.fn.modal.defaults, $this.data(), typeof option == 'object' && option)
      if (!data) $this.data('modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option]()
      else if (options.show) data.show()
    })
  }

  $.fn.modal.defaults = {
      backdrop: true
    , keyboard: true
    , show: true
  }

  $.fn.modal.Constructor = Modal


 /* MODAL DATA-API
  * ============== */

  $(function () {
    $('body').on('click.modal.data-api', '[data-toggle="modal"]', function ( e ) {
      var $this = $(this), href
        , $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) //strip for ie7
        , option = $target.data('modal') ? 'toggle' : $.extend({}, $target.data(), $this.data())

      e.preventDefault()
      $target.modal(option)
    })
  })

  // extends by ahern88
  var createBox = function(){
      $(".modal[id^=_myModal_]").remove();
      var $box = $('<div class="modal" id="_myModal_' + new Date().getTime() + '" style="display:none;">' +
                  '<div class="modal-header">' +
                    '<a class="close" data-dismiss="modal">×</a>' +
                    '<h3 id="_title">对话框标题</h3>' +
                  '</div>' +
                  '<div class="modal-body" id="_content">' +
                    '<p>对话框内容</p>' +
                  '</div>' +
                  '<div class="modal-footer">' +
                    '<a href="javascript:void(0);" class="btn" data-dismiss="modal" id="_cancel">取消</a>' +
                    '<a href="javascript:void(0);" class="btn btn-primary" id="_ok">确定</a>' +
                  '</div>' +
                '</div>');
      $box.appendTo("body").css({"position": "absolute", "left": "50%", "top": "50%", "margin-top": - $box.height()/2 + "px", "margin-left": - $box.width()/2 + "px"});
      return $box;
  };

  $.alert = function( message ) {
        var $box = createBox();
        $box.find("h3#_title").html("消息提示");
        $box.find("div#_content").html("<p>" + message + "</p>");
        $box.find("a#_cancel").remove();
        $box.find("a#_ok").unbind().click(function(){
          $box.find(".close").eq(0).click();
        });
        $box.modal({
          backdrop: "static"
        });
  };

  $.confirm = function (message, okfn) {
        var $box = createBox();
        $box.find("h3#_title").html("确认提示");
        $box.find("div#_content").html("<p>" + message + "</p>");
        $box.find("a#_ok").unbind().click(function(){
          okfn();
          $box.modal("hide");
        });
        $box.modal({
          backdrop: "static"
        });
  };

  $.box = function (options) {
        var $box = createBox();
        var defaults = {
          title: "信息显示",
          html: "",
          ok: "保存",
          okfn: function(){},
          cancel: "取消",
          height: "200px",
          width: "560px",
          params: {},
          cancelfn: function(){}
        };
        options = $.extend({}, defaults, options);
        $box.find("h3#_title").html(options.title);
        $box.find("div#_content").css({"height": options.height, "width": options.width}).html(options.html);
        for(var o in options.params){
            $("div#_content").find("#" + o).val(options.params[o]);
        }
        $box.css({"margin-top": - $box.height()/2 + "px"});
        $box.find("a#_ok").html(options.ok).unbind().click(function(){
          if(options.okfn())
              $box.modal("hide");
        });
        $box.find("a#_cancel").html(options.cancel).unbind().click(function(){
          if(options.cancelfn()){
              $box.modal("hide");
          }
        });
        $box.modal({
          backdrop: "static"
        });
  };

}( window.jQuery );