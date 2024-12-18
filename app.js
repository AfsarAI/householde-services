var app = new Vue({
  el: '#app',
  data: {
    msg: '', // Initially empty message
    submittedMsg: '' // To store the submitted message
  },
  methods: {
    submitMessage() {
      if (this.msg.trim() !== '') {
        this.submittedMsg = this.msg; // Save the message on submit
        this.msg = ''; // Clear the input field after submission
      } else {
        alert('Please enter a message before submitting!');
      }
    }
  }
});
